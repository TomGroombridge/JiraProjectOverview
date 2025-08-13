from datetime import datetime, timedelta
import requests
import os
from config import BANK_HOLIDAYS, SLACK_WEBHOOK_URL

def working_days_between(start_date, end_date, holidays=BANK_HOLIDAYS):
    """
    Returns a list of working days (Mon-Fri, excluding holidays) between two dates (inclusive).
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    delta = (end_date - start_date).days + 1
    all_days = [start_date + timedelta(days=i) for i in range(delta)]

    working_days = [
        d for d in all_days
        if d.weekday() < 5 and d.strftime("%Y-%m-%d") not in holidays
    ]
    return working_days


def send_direct_message(user_id, message, token):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": user_id,
        "text": message
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200 or not response.json().get("ok"):
        print("❌ Failed to send DM:", response.text)
    else:
        print("✅ DM sent successfully.")

def post_log_to_slack(log_path, webhook_url=SLACK_WEBHOOK_URL):
    if not webhook_url:
        print("No Slack webhook configured.")
        return

    if not os.path.exists(log_path):
        print("Log file not found.")
        return

    with open(log_path, 'r') as f:
        log_content = f.read()

    # Keep Slack message under 4000 chars (limit is ~4k)
    max_length = 3900
    log_snippet = log_content[-max_length:] if len(log_content) > max_length else log_content

    payload = {
        "text": f"*📊 Jira Epic Tracker Log ({datetime.now().strftime('%Y-%m-%d')}):*\n```{log_snippet}```"
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code != 200:
        print(f"⚠️ Slack post failed: {response.status_code} - {response.text}")
    else:
        print("✅ Log sent to Slack.")

