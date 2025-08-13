# 📊 Jira Project Tracker

This tool helps you track the progress of Jira epics by generating status breakdowns, velocity projections, dashboards, and logs. It is designed to be run daily to update an Excel progress log and optionally post updates to Slack.

---

## 🚀 Features

- Connects to Jira and fetches issues for an epic
- Filters out dropped tickets
- Calculates working days (excluding weekends, bank holidays, and developer leave)
- Assigns tickets to developers and estimates per-ticket effort
- Tracks velocity and projections
- Plots combined dashboard (bar + velocity line chart)
- Updates a historical Excel log (`project_progress_log.xlsx`)
- Posts logs to Slack
- Supports **multiple projects** via a `projects.yaml` config file

---

## 📁 File Structure

```
project-tracker/
├── main.py               # Entry point, runs tracking for each project
├── config/
│   └── projects.yaml     # Project-specific configuration
├── charts/
│   └── ...png            # Saved chart outputs
├── logs/
│   └── log.txt           # Daily summary log (optional Slack post)
├── output/
│   └── project_progress_log.xlsx  # Historical progress log
├── utils/
│   ├── jira.py           # Jira API integration
│   ├── analysis.py       # Ticket analysis and metrics
│   ├── charts.py         # Chart generation
│   ├── logging_utils.py  # File and Slack logging
│   └── helpers.py        # Common helper functions
└── .env                  # Your API secrets
```

---

## 🛠 Setup

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Set Up Environment Variables**

Create a `.env` file in your root directory with:

```env
JIRA_BASE_URL=https://yourcompany.atlassian.net
API_EMAIL=your@email.com
API_TOKEN=your_api_token
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...  # optional
SLACK_USER_ID=your_user_id
```

3. **Configure Projects in `projects.yaml`**

Located in the `config/` directory, this YAML file holds all project definitions.

```yaml
projects:
  - name: Project A
    epic_key: OBAU-31149
    start_date: 2025-08-04
    deadline: 2025-09-01
    developers:
      - name: OLENA
        leave: []
      - name: CHARLOTTE
        leave:
          - 2025-08-14
          - 2025-08-15
    bank_holidays:
      - 2025-08-25
```

You can define **as many projects as needed**, each with different:

- Epic keys
- Developer availability
- Bank holidays

---

## 🖼 Output

- `combined_project_dashboard.png`: status bar + velocity projection chart
- `project_progress_log.xlsx`: cumulative ticket progress over time
- `log.txt`: CLI summary (optional Slack post)

---

## 📅 Daily Automation (Cron)

Run the script daily at **8am** and post logs to Slack:

```bash
crontab -e
```

Add the following line:

```cron
0 8 * * * /usr/bin/python3 /full/path/to/main.py >> /full/path/to/logs/cron.log 2>&1
```

This will:

- Run your script every day at 8:00
- Append standard output and errors to a local cron log

---

## 🔔 Slack Integration

To post logs to Slack:

1. Set up an **Incoming Webhook** in your Slack workspace.
2. Add the `SLACK_WEBHOOK_URL` to your `.env`.
3. The script will send `log.txt` as a formatted message.

---

## ✨ Future Enhancements

- Highlight blocked or high-uncertainty tickets via Jira flags
- Visualise per-developer workload over time
- Add a web dashboard frontend
- Better classification of "quick wins" vs "unknowns"

---

## 📣 Contact

Made with ❤️ to help teams track progress and stay aligned.
