from datetime import datetime, timedelta
from config import DROPPED_STATUSES, STATUS_NORMALIZATION, INCLUDED_STATUSES, DEVELOPER_LEAVE, BANK_HOLIDAYS
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
        if issue['fields']['status']['name'] in {"Done", "Code Review"}
    )


def print_ticket_allocation_plan(issues, deadline, devs):
    today = datetime.today().date()
    end_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    working_days = working_days_between(today, end_date, BANK_HOLIDAYS)

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
        leave = set(DEVELOPER_LEAVE.get(dev, []))
        leave_days = [d for d in working_days if d.strftime("%Y-%m-%d") in leave]
        dev_availability[dev] = len(working_days) - len(leave_days)

    total_dev_days = sum(dev_availability.values())
    days_per_ticket = total_dev_days / total_tickets

    print(f"\n📋 Remaining tickets: {total_tickets}")
    print(f"👨‍💻 Developers: {', '.join(devs)}")
    print(f"🧮 Total available dev-days: {total_dev_days}")
    print(f"🕒 Average time per ticket: {days_per_ticket:.2f} days")

    dev_tickets = {dev: [] for dev in devs}
    for i, issue in enumerate(remaining):
        dev = devs[i % len(devs)]
        dev_tickets[dev].append(issue)
        print(f"  - {issue['key']}: \"{issue['fields']['summary']}\" → {days_per_ticket:.2f} days ({dev})")

    print("\n📦 Developer Workload Breakdown:")
    for dev in devs:
        ticket_count = len(dev_tickets[dev])
        dev_days = ticket_count * days_per_ticket
        print(f"  - {dev}: {dev_days:.2f} days for {ticket_count} tickets → {dev_availability[dev]} days available")


def print_velocity_summary(issues, deadline, start_date):
    today = datetime.today().date()
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(deadline, "%Y-%m-%d").date()

    total_issues = len([
        issue for issue in issues
        if issue['fields']['status']['name'] not in DROPPED_STATUSES
    ])
    done = count_done_tickets(issues)

    elapsed = len(working_days_between(start, today, BANK_HOLIDAYS))
    remaining = len(working_days_between(today, end, BANK_HOLIDAYS))
    total = elapsed + remaining

    actual_velocity = done / elapsed if elapsed > 0 else 0
    required_velocity = total_issues / total if total > 0 else 0
    projected_done = actual_velocity * total

    print("\n📈 Project Progress Report")
    print(f"  • Project start: {start_date}")
    print(f"  • Today: {today}")
    print(f"  • Tickets done: {done} / {total_issues}")
    print(f"  • Elapsed working days: {elapsed}")
    print(f"  • Remaining working days: {remaining}")
    print(f"  • Total working days: {total}")
    print(f"  • Velocity: {actual_velocity:.2f} (actual), {required_velocity:.2f} (required)")

    if projected_done >= total_issues:
        print(f"✅ Projected to finish with ~{projected_done:.1f} tickets — on track!")
    else:
        print(f"⚠️ Projected to finish with only ~{projected_done:.1f} tickets — behind schedule.")
