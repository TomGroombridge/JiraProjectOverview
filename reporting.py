import os
import pandas as pd
from datetime import datetime
from config import DROPPED_STATUSES
from metrics import count_done_tickets
from utils import working_days_between, get_project_output_dir


def update_progress_log_excel(issues, project_start_date, project_deadline, bank_holidays, project_name):
    output_dir = get_project_output_dir(project_name)
    excel_path = os.path.join(output_dir, "progress_log.xlsx")

    today = datetime.today().date()
    start = datetime.strptime(project_start_date, "%Y-%m-%d").date()
    end = datetime.strptime(project_deadline, "%Y-%m-%d").date()

    elapsed_days = len(working_days_between(start, today, bank_holidays))
    remaining_days = len(working_days_between(today, end, bank_holidays))
    total_days = elapsed_days + remaining_days

    total_tickets = len([
        i for i in issues
        if i['fields']['status']['name'] not in DROPPED_STATUSES
    ])
    done_tickets = count_done_tickets(issues)

    # Status breakdown
    status_count = {}
    for issue in issues:
        status = issue['fields']['status']['name']
        status_count[status] = status_count.get(status, 0) + 1

    todo = sum(status_count.get(s, 0) for s in ["To Do", "Backlog"])
    in_progress = status_count.get("In Progress", 0)
    code_review = status_count.get("Code Review", 0)
    done = status_count.get("Done", 0)
    dropped = sum(status_count.get(s, 0) for s in DROPPED_STATUSES)

    current_velocity = done_tickets / elapsed_days if elapsed_days > 0 else 0
    required_velocity = total_tickets / total_days if total_days > 0 else 0
    projected_done = current_velocity * total_days
    on_track = "Yes" if projected_done >= total_tickets else "No"

    row = {
        "Date": today.strftime("%Y-%m-%d"),
        "Total Tickets": total_tickets,
        "Tickets Completed": done_tickets,
        "Tickets Remaining": total_tickets - done_tickets,
        "To Do": todo,
        "In Progress": in_progress,
        "Code Review": code_review,
        "Done": done,
        "Dropped": dropped,
        "Days Elapsed": elapsed_days,
        "Days Remaining": remaining_days,
        "Current Velocity": round(current_velocity, 2),
        "Required Velocity": round(required_velocity, 2),
        "Projected Tickets Done": round(projected_done, 1),
        "On Track": on_track
    }

    try:
        df = pd.read_excel(excel_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([row])

    df.to_excel(excel_path, index=False)
    return df
