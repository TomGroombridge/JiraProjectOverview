from datetime import datetime, timedelta
from dateutil import parser
from config import DROPPED_STATUSES, STATUS_NORMALIZATION, INCLUDED_STATUSES
from utils import working_days_between


def count_statuses_excluding_dropped(issues):
    status_count = {}
    for issue in issues:
        status = issue['fields']['status']['name']
        if status in DROPPED_STATUSES:
            continue
        normalized = STATUS_NORMALIZATION.get(status, status)
        status_count[normalized] = status_count.get(normalized, 0) + 1
    return status_count


def count_done_tickets(issues):
    return sum(
        1 for issue in issues
        if issue['fields']['status']['name'] in {"Done", "Code Review", "Acceptance"}
    )

def count_in_progress_tickets(issues):
    return sum(
        1 for issue in issues
        if issue['fields']['status']['name'] in {"In Progress"}
    )

def get_time_in_progress(issue):
    changelog = issue.get("changelog", {}).get("histories", [])
    in_progress_time = None
    code_review_time = None

    for history in sorted(changelog, key=lambda x: x['created']):
        for item in history.get("items", []):
            if item.get("field") == "status":
                to_status = item.get("toString")
                timestamp = parser.parse(history["created"])
                
                if to_status == "In Progress" and in_progress_time is None:
                    in_progress_time = timestamp
                elif to_status in {"Code Review", "Done"} and in_progress_time:
                    code_review_time = timestamp
                    break  # We found both

    if in_progress_time and code_review_time:
        duration = code_review_time - in_progress_time
        return duration
    return None

def print_time_in_progress_summary(issues):
    print("\n✅ Completed Tickets, Time in Progress and Assignees:\n")
    for issue in issues:
        assignee = issue['fields']['assignee']
        assignee_name = assignee['displayName'] if assignee else "Unassigned"
        status = issue['fields']['status']['name']
        if status in {"Acceptance"}:
            key = issue['key']
            summary = issue['fields']['summary']
            duration = get_time_in_progress(issue)
            if duration:
                days = duration.days + duration.seconds / 86400  # include partial days
                print(f"  - {key}: \"{summary}\" → {days:.2f} days in progress → Assigned to: {assignee_name}")
            else:
                print(f"  - {key}: \"{summary}\" → No complete status transition data")


def print_ticket_allocation_plan(issues, deadline, devs, dev_leave, bank_holidays, project_name):
    today = datetime.today().date()
    end_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    working_days = working_days_between(today, end_date, bank_holidays)

    remaining = [
        issue for issue in issues
        if issue['fields']['status']['name'] in INCLUDED_STATUSES
    ]
    if not remaining:
        print("✅ No remaining tickets.")
        return

    total_tickets = len(remaining)

    dev_availability = {}
    for dev in devs:
        leave = set(dev_leave.get(dev, []))
        leave_days = [d for d in working_days if d in leave]
        dev_availability[dev] = len(working_days) - len(leave_days)

    total_dev_days = sum(dev_availability.values())
    days_per_ticket = total_dev_days / total_tickets

    print(f"\nℹ️  \033[1m{project_name} Project Overview\033[0m")
    print(f"📋 Remaining tickets: {total_tickets}")
    print(f"👨‍💻 Developers: {', '.join(devs)}")
    print(f"🧮 Total available dev-days: {total_dev_days}")
    print(f"🕒 Expected average time per ticket: {days_per_ticket:.2f} days")

    dev_tickets = {dev: [] for dev in devs}
    for i, issue in enumerate(remaining):
        dev = devs[i % len(devs)]
        dev_tickets[dev].append(issue)        

    print("\n📦 \033[1mDeveloper Workload Breakdown:\033[0m")
    for dev in devs:
        ticket_count = len(dev_tickets[dev])
        dev_days = ticket_count * days_per_ticket
        print(f"  - {dev}: {dev_availability[dev]} days available for {ticket_count} tickets")


def print_velocity_summary(issues, deadline, start_date, bank_holidays):
    today = datetime.today().date()
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(deadline, "%Y-%m-%d").date()

    total_issues = len([
        issue for issue in issues
        if issue['fields']['status']['name'] not in DROPPED_STATUSES
    ])
    done = count_done_tickets(issues)
    in_progress = count_in_progress_tickets(issues)

    elapsed = len(working_days_between(start, today, bank_holidays))
    remaining = len(working_days_between(today, end, bank_holidays))
    total = elapsed + remaining

    actual_velocity = done / elapsed if elapsed > 0 else 0
    required_velocity = total_issues / total if total > 0 else 0
    projected_done = actual_velocity * total

    print("\n📈 \033[1mProject Progress Report\033[0m")
    print(f"  • Project start: {start_date}")
    print(f"  • Today: {today}")
    print(f"  • Tickets done: {done} / {total_issues}")
    print(f"  • Tickets in progress: {in_progress}")
    print(f"  • Elapsed working days: {elapsed}")
    print(f"  • Remaining working days: {remaining}")    
    print(f"  • Velocity: {actual_velocity:.2f} (actual), {required_velocity:.2f} (required)")

    if projected_done >= total_issues:
        print(f"\n✅  Projected to finish with ~{projected_done:.1f} tickets — on track!")
    else:
        print(f"\n⚠️  Projected to finish with only ~{projected_done:.1f} tickets — \033[91mBehind Schedule.\033[0m")
