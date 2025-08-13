# 📊 Jira Epic Tracker

This tool allows you to track the progress of Jira epics over time, generating visual dashboards and maintaining an Excel log of daily progress. It supports multiple projects, developer availability, bank holidays, and Slack notifications.

---

## 🚀 Features

- Fetch issues from a Jira epic
- Track issue statuses (To Do, In Progress, Code Review, Done, etc.)
- Account for bank holidays and individual developer leave
- Estimate average time available per ticket
- Generate visual dashboards (bar + line charts)
- Maintain a time-series Excel log
- Automatically run daily using `cron`
- Post daily logs to Slack (optional)
- Support for **multiple projects** via `projects.yaml`
- Project-specific output folders

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-org/jira-epic-tracker.git
cd jira-epic-tracker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file:

```env
JIRA_BASE_URL=https://your-domain.atlassian.net
API_EMAIL=your.email@example.com
API_TOKEN=your_api_token
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url
```

> 🔐 Your `.env` file is automatically ignored by Git. Don’t commit secrets.

### 4. Create your `projects.yaml`

```yaml
projects:
  - name: My First Project
    epic_key: OBAU-12345
    start_date: 2025-08-04
    end_date: 2025-09-01
    developers:
      - name: Olena
        leave:
          - 2025-08-14
      - name: Charlotte
        leave:
          - 2025-08-15
    bank_holidays:
      - 2025-08-26

  - name: My Second Project
    epic_key: OBAU-67890
    start_date: 2025-08-01
    end_date: 2025-09-15
    developers:
      - name: Alice
        leave: []
    bank_holidays:
      - 2025-08-26
      - 2025-09-02
```

---

## 🖥️ Running the script manually

```bash
python main.py
```

This will:

- Fetch and analyze each project
- Generate updated Excel log at: `outputs/{project_name}/progress_log.xlsx`
- Save dashboard images to: `outputs/{project_name}/dashboard_YYYY-MM-DD.png`
- Optionally post results to Slack

---

## 📅 Running daily via cron

### 1. Edit your crontab

```bash
crontab -e
```

### 2. Add the following line to run the script at 8:00 AM daily:

```cron
0 8 * * * /usr/bin/python3 /path/to/your/project/main.py >> /path/to/your/project/log.txt 2>&1
```

> Replace `/usr/bin/python3` and `/path/to/your/project/` with your actual Python path and script location.

### 3. Confirm it's scheduled

```bash
crontab -l
```

### ✅ View logs

Output is appended to `log.txt`. You can check this file to confirm the cron job ran successfully.

---

## 💬 Slack Integration

To post updates to Slack:

1. [Create an Incoming Webhook](https://api.slack.com/messaging/webhooks) for your Slack workspace
2. Paste the webhook URL into your `.env` file as `SLACK_WEBHOOK_URL`
3. The script will automatically post daily logs to Slack if this variable is present.

> Note: You can only send messages to channels the app is a member of. DM support is limited via webhooks.

---

## 📁 Output Structure

```
outputs/
├── my_first_project/
│   ├── dashboard_2025-08-14.png
│   └── progress_log.xlsx
├── my_second_project/
│   ├── dashboard_2025-08-14.png
│   └── progress_log.xlsx
```

---

## ✅ Status Order

Bar charts always follow the Jira status flow:

```python
JIRA_STATUS_ORDER = ["Backlog", "To Do", "In Progress", "Code Review", "Done", "Dropped"]
```

---

## 👏 Contributions

Feel free to submit issues or pull requests to improve functionality or extend support for additional tools.

---

## License

MIT
