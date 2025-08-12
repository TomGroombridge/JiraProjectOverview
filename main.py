from config import EPIC_KEY, PROJECT_START_DATE, PROJECT_DEADLINE, DROPPED_STATUSES, DEVS
from jira_client import get_issues_in_epic
from metrics import (
    print_ticket_allocation_plan,
    print_velocity_summary,
    count_statuses_excluding_dropped
)
from charts import plot_combined_status_dashboard
from reporting import update_progress_log_excel


def main():
    print(f"Fetching issues for Epic {EPIC_KEY}...")
    issues = get_issues_in_epic(EPIC_KEY)
    print(f"Found {len(issues)} issues.")

    print_ticket_allocation_plan(issues, PROJECT_DEADLINE, DEVS)
    print_velocity_summary(issues, PROJECT_DEADLINE, PROJECT_START_DATE)

    status_count = count_statuses_excluding_dropped(issues)

    update_progress_log_excel(
        issues=issues,
        excel_path="project_progress_log.xlsx",
        project_start_date=PROJECT_START_DATE,
        project_deadline=PROJECT_DEADLINE
    )

    plot_combined_status_dashboard(
        issues=issues,
        epic_key=EPIC_KEY,
        project_start_date=PROJECT_START_DATE,
        deadline=PROJECT_DEADLINE,
        status_count=status_count,
        dropped_statuses=DROPPED_STATUSES
    )


if __name__ == "__main__":
    main()
