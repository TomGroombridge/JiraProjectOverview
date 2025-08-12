# Jira Project Tracker

A lightweight Python tool for tracking Jira epic progress and producing visual + tabular reports.
Ideal for sharing project insights with non-technical stakeholders.

---

## 🚀 Features

- Fetches all tickets from a specified Jira epic
- Excludes dropped/cancelled tickets
- Normalizes statuses (e.g. "Backlog" + "To Do")
- Tracks developer capacity (including holidays)
- Calculates required vs actual ticket velocity
- Visualizes:

  - ✅ Status breakdown bar chart
  - 📈 Progress vs. required velocity line chart

- Updates a cumulative Excel progress log daily

---

## 📁 Project Structure

```
jira_project_tracker/
├── main.py                  # Entry point
├── config.py                # Project config and developer metadata
├── jira_client.py           # Jira API access
├── metrics.py               # Velocity & allocation calculations
├── charts.py                # Status + velocity visualizations
├── reporting.py             # Excel output log
├── utils.py                 # Shared working days calculator
├── .env                     # Private environment variables (not committed)
├── requirements.txt         # Required Python packages
└── project_progress_log.xlsx # Daily progress log (auto-generated)
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-org/jira-project-tracker.git
cd jira-project-tracker
```

### 2. Create a `.env` file

```env
JIRA_BASE_URL=https://yourcompany.atlassian.net
API_EMAIL=your.email@company.com
API_TOKEN=your_generated_api_token
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the script

```bash
python main.py
```

---

## 📊 Output

- `combined_project_dashboard.png` — visual dashboard (status bar + velocity line chart)
- `project_progress_log.xlsx` — running history of project metrics over time

---

## 🧩 Customization

Modify `config.py` to:

- Change `EPIC_KEY`, `PROJECT_START_DATE`, or `PROJECT_DEADLINE`
- Add developer names & leave dates
- Add or remove bank holidays
- Normalize custom Jira statuses

---

## 🛡️ Environment Management

Never commit sensitive credentials. Use `.env` with `python-dotenv`.

Add `.env` to your `.gitignore`:

```bash
echo ".env" >> .gitignore
```

---

## ⏰ Automation Tip

Use a cron job or GitHub Actions to run the script daily and track project velocity automatically.

---

## 📝 License

MIT or your preferred open license.

---

## 🙋‍♂️ Questions?

Feel free to open an issue or contact the author.

---

**Built with ❤️ for project visibility and delivery clarity.**
