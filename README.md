# 📊 Jira Epic Progress Tracker

This Python tool helps track the progress of a Jira Epic by:

- Fetching tickets from a specified epic
- Generating visual dashboards (bar + velocity charts)
- Estimating delivery timelines based on developer availability
- Logging daily progress into an Excel file

---

## 📦 Requirements

- Python 3.8+
- Jira API access with email/token
- A `.env` file with your secrets (see below)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Setup

### 1. Clone this repo and install dependencies

### 2. Add a `.env` file in the root:

```ini
JIRA_BASE_URL=https://jira.yourdomain.com
API_EMAIL=your.email@company.com
API_TOKEN=your_api_token
```

### 3. Configure your `main.py`

Update constants like:

- `EPIC_KEY`
- `PROJECT_START_DATE`
- Developer names & leave dates

---

## 🛠️ Usage

Run it manually with:

```bash
python main.py
```

This will:

- Fetch the issues
- Generate dashboard charts
- Print insights to terminal
- Update `project_progress_log.xlsx`

---

## 🧮 Output

### ✅ Generates:

- `combined_project_dashboard.png`: Bar + line chart
- `project_progress_log.xlsx`: Daily cumulative report

### 📊 Excel Columns Tracked:

- Date
- Total tickets / completed / remaining
- Status breakdown (To Do, In Progress, etc.)
- Velocity (current vs required)
- On track: Yes/No

---

## ⏱️ Automate with Cron (Optional)

To run the script daily at **8:00 AM**, add this line to your crontab:

```bash
crontab -e
```

Then add:

```cron
0 8 * * * /usr/bin/env bash -c 'cd /absolute/path/to/project && /usr/bin/env python3 main.py >> log.txt 2>&1'
```

This will:

- Run the script at 5:05 PM every day
- Append logs to `log.txt`

✅ Tip: Use `tail -f log.txt` to watch it live.

---

## 🧠 Optional Enhancements

- Add `unknowns` or `easy-win` Jira labels to flag ticket complexity
- Visualise ticket effort vs uncertainty in charts
- Extend to multiple epics or projects

---

## 🛡️ Security

Ensure `.env` and `project_progress_log.xlsx` are in `.gitignore` to prevent sensitive info from being committed.

---

## 🙌 Credits

Built for Zopa Engineering to track project progress with clarity and flexibility.
