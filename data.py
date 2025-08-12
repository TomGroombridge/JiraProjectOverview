import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta


load_dotenv()
# CONFIGURE THESE
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
API_EMAIL = os.getenv("API_EMAIL")
API_TOKEN = os.getenv("API_TOKEN")
EPIC_KEY = "OBAU-31149"
PROJECT_START_DATE = "2025-08-04"
DROPPED_STATUSES = {"Dropped", "Cancelled", "Won't Do"}
INCLUDED_STATUSES = {"To Do", "Backlog", "In Progress"}
DEV_A = 'OLENA'
DEV_B = 'CHARLOTTE'
DEVELOPER_LEAVE = {
    "OLENA": [],
    "CHARLOTTE": ["2025-08-14", "2025-08-15"]
}
STATUS_NORMALIZATION = {
    "Backlog": "To Do",
    "To Do": "To Do"
    # Add more mappings if needed
}
BANK_HOLIDAYS = {
    "2025-08-25",  # Summer bank holiday (Monday)
}

# Simple headers
headers = {
    "Accept": "application/json"
}

def get_issues_in_epic(epic_key):
    jql = f'"Epic Link" = "{epic_key}"'
    url = f"{JIRA_BASE_URL}/rest/api/2/search"
    params = {
        "jql": jql,
        "fields": "summary,status,issuetype"
    }
    response = requests.get(url, headers=headers, params=params,
                            auth=HTTPBasicAuth(API_EMAIL, API_TOKEN))
    response.raise_for_status()
    # print('DATA:', response.json())
    # print('DATA:', json.dumps(response.json(), indent=2))
    return response.json()['issues']

def count_statuses(issues):
    status_count = {}
    for issue in issues:
        status = issue['fields']['status']['name']
        status_count[status] = status_count.get(status, 0) + 1
    return status_count

def count_statuses_excluding_dropped(issues):
    status_count = {}
    for issue in issues:
        status = issue['fields']['status']['name']
        
        # Skip dropped statuses
        if status in DROPPED_STATUSES:
            continue
        
        # Normalize status
        normalized_status = STATUS_NORMALIZATION.get(status, status)
        
        # Count it
        status_count[normalized_status] = status_count.get(normalized_status, 0) + 1

    return status_count

def working_days_until(deadline):
    today = datetime.today().date()
    end_date = datetime.strptime(deadline, "%Y-%m-%d").date()

    if end_date <= today:
        return 0

    delta = (end_date - today).days + 1
    days = [today + timedelta(days=i) for i in range(delta)]

    working_days = [
        d for d in days 
        if d.weekday() < 5 and d.strftime("%Y-%m-%d") not in BANK_HOLIDAYS
    ]

    return len(working_days)

def print_ticket_deadline_breakdown(issues, deadline, devs=("OLENA", "CHARLOTTE")):
    remaining_tickets = [
        issue for issue in issues
        if issue['fields']['status']['name'] in INCLUDED_STATUSES
    ]

    total_tickets = len(remaining_tickets)
    if total_tickets == 0:
        print("✅ No remaining tickets.")
        return

    # Get working days from today to deadline
    today = datetime.today().date()
    end_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    delta = (end_date - today).days + 1
    all_days = [today + timedelta(days=i) for i in range(delta)]
    working_days = [d for d in all_days if d.weekday() < 5 and d.strftime("%Y-%m-%d") not in BANK_HOLIDAYS]

    # Count available days per developer
    dev_availability = {}
    for dev in devs:
        leave_dates = set(DEVELOPER_LEAVE.get(dev, []))
        leave_days = [d for d in working_days if d.strftime("%Y-%m-%d") in leave_dates]
        available_days = len(working_days) - len(leave_days)
        dev_availability[dev] = available_days

    # Total available dev-days
    total_available_dev_days = sum(dev_availability.values())
    days_per_ticket = total_available_dev_days / total_tickets

    print(f"\n📅 Total working days (excluding weekends + bank holidays): {len(working_days)}")
    print(f"📋 Remaining tickets: {total_tickets}")
    print(f"👨‍💻 Developers: {', '.join(devs)}")
    print(f"🧮 Total developer-days available (after leave): {total_available_dev_days}")
    print(f"🧮 Each ticket can take ~{days_per_ticket:.2f} days (on average)\n")

    # Assign tickets round-robin
    dev_tickets = {dev: [] for dev in devs}
    for idx, issue in enumerate(remaining_tickets):
        assigned_dev = devs[idx % len(devs)]
        dev_tickets[assigned_dev].append(issue)
        key = issue['key']
        summary = issue['fields']['summary']
        print(f"  - {key}: \"{summary}\" → {days_per_ticket:.2f} days ({assigned_dev})")

    # Per-dev workload
    print("\n📦 Developer Workload Breakdown:")
    for dev in devs:
        tickets = dev_tickets[dev]
        dev_days = len(tickets) * days_per_ticket
        print(f"  - {dev}: {dev_days:.2f} days across {len(tickets)} tickets → {dev_availability[dev]} days available (after leave)")

def working_days_between(start_date, end_date):
    delta = (end_date - start_date).days + 1
    all_days = [start_date + timedelta(days=i) for i in range(delta)]
    return [
        d for d in all_days
        if d.weekday() < 5 and d.strftime("%Y-%m-%d") not in BANK_HOLIDAYS
    ]

def count_done_tickets(issues):
    return sum(
        1 for issue in issues
        if issue['fields']['status']['name'] in {"Done", "Code Review"}
    )

def print_progress_vs_expectation(issues, deadline, project_start_date):
    today = datetime.today().date()
    start_date = datetime.strptime(project_start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(deadline, "%Y-%m-%d").date()

    total_tickets = len([
        issue for issue in issues
        if issue['fields']['status']['name'] not in DROPPED_STATUSES
    ])

    done_tickets = count_done_tickets(issues)
    elapsed_working_days = len(working_days_between(start_date, today))
    remaining_working_days = len(working_days_between(today, end_date))

    # Current velocity
    if elapsed_working_days > 0:
        actual_velocity = done_tickets / elapsed_working_days
    else:
        actual_velocity = 0

    # Expected total ticket velocity to finish all work
    total_working_days = elapsed_working_days + remaining_working_days
    expected_velocity = total_tickets / total_working_days if total_working_days else 0

    # Projection
    projected_total_done = actual_velocity * total_working_days

    print(f"\n📈 Project Progress Report")
    print(f"  • Project start date: {project_start_date}")
    print(f"  • Today: {today}")
    print(f"  • Tickets completed: {done_tickets} of {total_tickets}")
    print(f"  • Elapsed working days: {elapsed_working_days}")
    print(f"  • Remaining working days: {remaining_working_days}")
    print(f"  • Total working days: {total_working_days}")
    print(f"  • Current velocity: {actual_velocity:.2f} tickets/day")
    print(f"  • Required velocity: {expected_velocity:.2f} tickets/day")

    if projected_total_done >= total_tickets:
        print(f"✅ At current pace, you're projected to complete ~{projected_total_done:.1f} tickets — you’re on track or ahead!")
    else:
        print(f"⚠️ At current pace, you’ll likely complete only ~{projected_total_done:.1f} tickets — consider adjusting scope or pace.")

def plot_bar_chart(status_count, epic_key):
    statuses = list(status_count.keys())
    counts = [status_count[status] for status in statuses]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(statuses, counts)
    
    plt.title(f"Issue Status for Epic {epic_key}")
    plt.xlabel("Status")
    plt.ylabel("Number of Issues")

    # Add labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height, f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(f"{epic_key}_status_chart.png")
    plt.show()

def plot_velocity_comparison(issues, project_start, deadline):
    start_date = datetime.strptime(project_start, "%Y-%m-%d").date()
    end_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    today = datetime.today().date()

    # Get working days from start to deadline
    working_days = working_days_between(start_date, end_date)
    elapsed_days = working_days_between(start_date, today)

    total_tickets = len([
        issue for issue in issues
        if issue['fields']['status']['name'] not in DROPPED_STATUSES
    ])

    done_count = count_done_tickets(issues)

    # Build required velocity line
    required_line = [
        (i / (len(working_days) - 1)) * total_tickets for i in range(len(working_days))
    ]

    # Simulated actual line: spread completed tickets evenly across elapsed days
    actual_line = []
    for i in range(len(working_days)):
        if i < len(elapsed_days):
            value = (i / len(elapsed_days)) * done_count
        else:
            value = done_count
        actual_line.append(value)

    # Plotting
    x_labels = [d.strftime("%b %d") for d in working_days]
    plt.figure(figsize=(12, 6))
    plt.plot(x_labels, required_line, label="Required Velocity", linestyle='--', color='gray')
    plt.plot(x_labels, actual_line, label="Actual Progress", marker='o')

    plt.xticks(rotation=45)
    plt.xlabel("Working Days")
    plt.ylabel("Cumulative Tickets Completed")
    plt.title("Actual vs Required Velocity")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.savefig("velocity_comparison.png")
    plt.show()

def generate_project_dashboard(
    issues,
    epic_key,
    project_start_date,
    deadline,
    status_count,
    dropped_statuses,
):
    # Convert date strings
    start_date = datetime.strptime(project_start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    today = datetime.today().date()

    # Working day helpers
    def working_days_between(start, end):
        delta = (end - start).days + 1
        all_days = [start + timedelta(days=i) for i in range(delta)]
        return [
            d for d in all_days
            if d.weekday() < 5 and d.strftime("%Y-%m-%d") not in BANK_HOLIDAYS
        ]

    # Get working days from start to deadline and until today
    all_working_days = working_days_between(start_date, end_date)
    elapsed_working_days = working_days_between(start_date, today)
    x_labels = [d.strftime("%b %d") for d in all_working_days]

    # Count total tickets excluding dropped
    total_tickets = len([
        i for i in issues
        if i['fields']['status']['name'] not in dropped_statuses
    ])

    # Count done + code review tickets
    done_tickets = sum(
        1 for i in issues
        if i['fields']['status']['name'] in {"Done", "Code Review"}
    )

    # Required velocity: linear completion line
    required_line = [
        (i / (len(all_working_days) - 1)) * total_tickets
        for i in range(len(all_working_days))
    ]

    # Actual velocity projection line
    days_elapsed = len(elapsed_working_days)
    actual_velocity = done_tickets / days_elapsed if days_elapsed > 0 else 0

    actual_line = []
    for i in range(len(all_working_days)):
        projected = actual_velocity * i
        capped = min(projected, total_tickets)  # Prevent going over
        actual_line.append(capped)

    # === Plot charts ===
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 row, 2 columns

    # === Bar Chart: Ticket Statuses ===
    statuses = list(status_count.keys())
    counts = [status_count[s] for s in statuses]
    bars = axes[0].bar(statuses, counts, color='steelblue')
    axes[0].set_title(f"Issue Status for Epic {epic_key}")
    axes[0].set_xlabel("Status")
    axes[0].set_ylabel("Number of Issues")
    for bar in bars:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(height)}',
                     ha='center', va='bottom')

    # === Line Chart: Velocity Projection ===
    axes[1].plot(x_labels, required_line, label="Required Velocity", linestyle='--', color='gray')
    axes[1].plot(x_labels, actual_line, label="Actual Progress", marker='o', color='dodgerblue')
    axes[1].set_title("Actual vs Required Velocity")
    axes[1].set_xlabel("Working Days")
    axes[1].set_ylabel("Cumulative Tickets Completed")
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig("combined_project_dashboard.png")
    plt.show()

def update_progress_log_excel(
    issues,
    excel_path,
    project_start_date,
    project_deadline
):
    DROPPED_STATUSES = {"Dropped", "Cancelled", "Won't Do"}
    BANK_HOLIDAYS = {"2025-08-25"}

    # Utility functions
    def working_days_between(start_date, end_date):
        delta = (end_date - start_date).days + 1
        all_days = [start_date + timedelta(days=i) for i in range(delta)]
        return [
            d for d in all_days
            if d.weekday() < 5 and d.strftime("%Y-%m-%d") not in BANK_HOLIDAYS
        ]

    def count_done_tickets(issues):
        return sum(
            1 for issue in issues
            if issue['fields']['status']['name'] in {"Done", "Code Review"}
        )

    def count_statuses(issues):
        status_count = {}
        for issue in issues:
            status = issue['fields']['status']['name']
            status_count[status] = status_count.get(status, 0) + 1
        return status_count

    # Date setup
    today = datetime.today().date()
    start_date = datetime.strptime(project_start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(project_deadline, "%Y-%m-%d").date()

    # Working day calculations
    elapsed_working_days = len(working_days_between(start_date, today))
    remaining_working_days = len(working_days_between(today, end_date))
    total_working_days = elapsed_working_days + remaining_working_days

    # Ticket counts
    total_tickets = len([i for i in issues if i['fields']['status']['name'] not in DROPPED_STATUSES])
    done_tickets = count_done_tickets(issues)

    status_counts = count_statuses(issues)
    todo = sum(status_counts.get(status, 0) for status in ["To Do", "Backlog"])
    in_progress = status_counts.get("In Progress", 0)
    code_review = status_counts.get("Code Review", 0)
    done = status_counts.get("Done", 0)
    dropped = sum(status_counts.get(status, 0) for status in DROPPED_STATUSES)

    tickets_completed = done_tickets
    tickets_remaining = total_tickets - tickets_completed

    # Velocity calculations
    current_velocity = tickets_completed / elapsed_working_days if elapsed_working_days > 0 else 0
    required_velocity = total_tickets / total_working_days if total_working_days > 0 else 0
    projected_total_done = current_velocity * total_working_days
    on_track = "Yes" if projected_total_done >= total_tickets else "No"

    # Create daily snapshot row
    snapshot_df = pd.DataFrame([{
        "Date": today.strftime("%Y-%m-%d"),
        "Total Tickets": total_tickets,
        "Tickets Completed": tickets_completed,
        "Tickets Remaining": tickets_remaining,
        "To Do": todo,
        "In Progress": in_progress,
        "Code Review": code_review,
        "Done": done,
        "Dropped": dropped,
        "Days Elapsed": elapsed_working_days,
        "Days Remaining": remaining_working_days,
        "Current Velocity": round(current_velocity, 2),
        "Required Velocity": round(required_velocity, 2),
        "Projected Tickets Done": round(projected_total_done, 1),
        "On Track": on_track
    }])

    # Load existing log or start new
    try:
        existing_df = pd.read_excel(excel_path)
        updated_df = pd.concat([existing_df, snapshot_df], ignore_index=True)
    except FileNotFoundError:
        updated_df = snapshot_df

    # Save log
    updated_df.to_excel(excel_path, index=False)
    return updated_df

def main():
    print(f"Fetching issues for Epic {EPIC_KEY}...")
    issues = get_issues_in_epic(EPIC_KEY)
    print(f"Found {len(issues)} issues.")
    deadline = "2025-09-01"
    print_ticket_deadline_breakdown(issues, deadline)

    print_progress_vs_expectation(issues, deadline="2025-09-01", project_start_date=PROJECT_START_DATE)

    status_count = count_statuses_excluding_dropped(issues)
    # print("Status breakdown:", status_count)
    # plot_bar_chart(status_count, EPIC_KEY)

    # plot_velocity_comparison(issues, project_start=PROJECT_START_DATE, deadline="2025-09-01")

    update_progress_log_excel(
        issues=issues,
        excel_path="project_progress_log.xlsx",
        project_start_date=PROJECT_START_DATE,
        project_deadline="2025-09-01"
    )
    generate_project_dashboard(
    issues=issues,
    epic_key=EPIC_KEY,
    project_start_date=PROJECT_START_DATE,
    deadline="2025-09-01",
    status_count=status_count,
    dropped_statuses=DROPPED_STATUSES

)

if __name__ == "__main__":
    main()