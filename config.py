import os
from dotenv import load_dotenv

load_dotenv()

# Jira Auth
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
API_EMAIL = os.getenv("API_EMAIL")
API_TOKEN = os.getenv("API_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_USER_ID = os.getenv("SLACK_USER_ID")

# Statuses
DROPPED_STATUSES = {"Dropped", "Cancelled", "Won't Do"}
INCLUDED_STATUSES = {"To Do", "Backlog", "In Progress", "Ready for production"}
STATUS_NORMALIZATION = {
    "Backlog": "To Do",
    "To Do": "To Do"
}

