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

# Project Setup
EPIC_KEY = "OBAU-31149"
PROJECT_START_DATE = "2025-08-04"
PROJECT_DEADLINE = "2025-09-01"

# Statuses
DROPPED_STATUSES = {"Dropped", "Cancelled", "Won't Do"}
INCLUDED_STATUSES = {"To Do", "Backlog", "In Progress"}
STATUS_NORMALIZATION = {
    "Backlog": "To Do",
    "To Do": "To Do"
}

# Team
DEVS = ["OLENA", "CHARLOTTE"]
DEVELOPER_LEAVE = {
    "OLENA": [],
    "CHARLOTTE": ["2025-08-14", "2025-08-15", "2025-08-28", "2025-08-29"]
}

# UK Bank Holidays (can be expanded)
BANK_HOLIDAYS = {"2025-08-25"}