from config import DROPPED_STATUSES, SLACK_BOT_TOKEN, SLACK_USER_ID
from jira_client import get_issues_in_epic
from metrics import (
    print_ticket_allocation_plan,
    print_velocity_summary,
    count_statuses_excluding_dropped,    
    print_time_in_progress_summary
)
from utils import post_log_to_slack, send_direct_message, load_project_configs
from charts import plot_combined_status_dashboard
from reporting import update_progress_log_excel



def main():
    projects = load_project_configs()

    for project in projects:
        epic_key = project["epic_key"]
        epic_name = project["name"]
        deadline = project["deadline"]
        start_date = project["start_date"]
        start_date = project["start_date"]
        developers = [dev["name"] for dev in project["developers"]]
        dev_leave = {dev["name"]: dev.get("leave", []) for dev in project["developers"]}
        bank_holidays = set(project["bank_holidays"])
        
        print(f"Fetching issues for Epic {epic_key}...")
        issues = get_issues_in_epic(epic_key)
        print_ticket_allocation_plan(issues, deadline, developers, dev_leave, bank_holidays, epic_name)
        print_velocity_summary(issues, deadline, start_date, bank_holidays)    
        print_time_in_progress_summary(issues)
        status_count = count_statuses_excluding_dropped(issues)

        update_progress_log_excel(
            issues=issues,            
            project_start_date=start_date,
            project_deadline=deadline,
            bank_holidays=bank_holidays,
            project_name=epic_name
        )

        plot_combined_status_dashboard(
            issues=issues,
            epic_key=epic_key,
            project_start_date=start_date,
            deadline=deadline,
            status_count=status_count,
            dropped_statuses=DROPPED_STATUSES,
            bank_holidays=bank_holidays,
            project_name=epic_name
        )
        print(f"\n\n")
        print(f"----------------------------------------------------------------------------")
        print(f"\n\n\n\n")
        # send_direct_message(SLACK_USER_ID, 'TEST MESSAGE', SLACK_BOT_TOKEN)
        # post_log_to_slack("log.txt")


if __name__ == "__main__":
    main()
