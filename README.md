# Jira Epic Tracker

This tool tracks the progress of a Jira Epic and generates daily reports, charts, and projections. It logs key metrics to an Excel file and provides visual dashboards, helping both technical and non-technical stakeholders understand project health.

---

## ✅ Features

- Fetches Jira issues in a specific Epic
- Tracks ticket status breakdown (excluding "Dropped" statuses)
- Projects ticket workload per developer
- Calculates working days excluding weekends, bank holidays, and developer leave
- Estimates current vs required ticket velocity
- Generates charts for status distribution and progress tracking
- Saves daily snapshots to `project_progress_log.xlsx`
- Supports Slack notifications with `log.txt` content

---

## 🧰 Prerequisites

- Python 3.8+
- Jira API token
- A `.env` file with credentials (see below)
- Install required packages:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```dotenv
JIRA_BASE_URL=https://your-jira-instance.atlassian.net
API_EMAIL=your.email@company.com
API_TOKEN=your_jira_api_token
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
SLACK_USER_ID=your_user_id
```

---

## 📊 Output

Each daily run will:

- Update `project_progress_log.xlsx`
- Save updated dashboard charts to `combined_project_dashboard.png`
- Post summary logs to Slack (if configured)

---

## 📅 Set Up Daily Run (via Cron)

To run the script every day at **8:00 AM**:

```bash
crontab -e
```

Add:

```cron
0 8 * * * /usr/bin/env bash -c 'cd /absolute/path/to/project && /usr/bin/env python3 main.py >> log.txt 2>&1'
```

This will:

- Navigate to the project folder
- Run `main.py`
- Append output to `log.txt`

---

## 🔔 Slack Integration

The script supports sending logs to Slack using **Incoming Webhooks**.

1. Go to [Slack App Management](https://api.slack.com/apps)
2. Create a new app → Incoming Webhooks
3. Add a webhook and select the channel
4. Paste the webhook URL into your `.env` file

Slack messages are posted with the content of `log.txt`.

> **Note**: Due to Slack limitations, webhook messages cannot send direct messages to users. They post into channels.

---

## 📝 Log Fields in `project_progress_log.xlsx`

- Date
- Total Tickets
- Tickets Completed
- Tickets Remaining
- To Do
- In Progress
- Code Review
- Done
- Dropped
- Days Elapsed
- Days Remaining
- Current Velocity
- Required Velocity
- Projected Tickets Done
- On Track

---

## 🧠 Coming Enhancements (Ideas)

- Identify tickets with high uncertainty or complexity
- Show average time in each status per ticket
- Include links to tickets in reports
- Flag overdue or stagnating issues

---

## 📂 File Structure

```bash
.
├── charts/                     # Saved images (bar + velocity charts)
├── logs/
│   └── log.txt                # Output of cron script
├── main.py                    # Main execution script
├── jira_api.py                # Fetch issues & changelogs
├── analytics.py               # Projections & estimations
├── visualisations.py          # Chart generation
├── reporting.py               # Excel export & Slack posting
├── utils.py                   # Shared helper functions
├── .env                       # Environment variables
├── requirements.txt
└── README.md
```

---

## 💬 Questions or Suggestions?

Open an issue or drop a message in the team channel.

---

Made with 💙 to bring visibility to your Jira epics.
