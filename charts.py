import matplotlib.pyplot as plt
import os
from datetime import datetime
from utils import working_days_between, get_project_output_dir
from metrics import count_done_tickets

JIRA_STATUS_ORDER = ["To Do", "In Progress", "Code Review", "Acceptance", "Ready for production", "Done"]


def plot_combined_status_dashboard(
    issues,
    epic_key,
    project_start_date,
    deadline,
    status_count,
    dropped_statuses,
    bank_holidays,
    project_name
):
    start_date = datetime.strptime(project_start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    today = datetime.today().date()

    all_days = working_days_between(start_date, end_date, bank_holidays)
    elapsed_days = working_days_between(start_date, today, bank_holidays)
    x_labels = [d.strftime("%b %d") for d in all_days]

    total_tickets = len([
        i for i in issues
        if i['fields']['status']['name'] not in dropped_statuses
    ])
    done_tickets = count_done_tickets(issues)

    # Required line (linear projection)
    required_line = [
        (i / (len(all_days) - 1)) * total_tickets
        for i in range(len(all_days))
    ]

    # Actual line (projected forward at current velocity)
    velocity = done_tickets / len(elapsed_days) if elapsed_days else 0
    actual_line = [min(i * velocity, total_tickets) for i in range(len(all_days))]

    # Chart layout
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # === Bar Chart ===    

    sorted_statuses = [s for s in JIRA_STATUS_ORDER if s in status_count]
    counts = [status_count[s] for s in sorted_statuses]
    bars = axes[0].bar(sorted_statuses, counts, color='steelblue')
    axes[0].set_title(f"Status Breakdown for Epic {epic_key}")
    axes[0].set_xlabel("Status")
    axes[0].set_ylabel("Count")
    for bar in bars:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2.0, height, f'{int(height)}',
                     ha='center', va='bottom')

    # === Line Chart ===
    axes[1].plot(x_labels, required_line, label="Required Velocity", linestyle='--', color='gray')
    axes[1].plot(x_labels, actual_line, label="Actual Progress", marker='o', color='dodgerblue')
    axes[1].set_title("Actual vs Required Velocity")
    axes[1].set_xlabel("Working Days")
    axes[1].set_ylabel("Cumulative Tickets Completed")
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()

    output_dir = get_project_output_dir(project_name)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    chart_path = os.path.join(output_dir, f"dashboard_{timestamp}.png")
    plt.savefig(chart_path)
    plt.close()    
