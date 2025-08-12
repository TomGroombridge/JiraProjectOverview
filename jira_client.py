import requests
from requests.auth import HTTPBasicAuth
from config import JIRA_BASE_URL, API_EMAIL, API_TOKEN

HEADERS = {
    "Accept": "application/json"
}

def get_issues_in_epic(epic_key):
    jql = f'"Epic Link" = "{epic_key}"'
    url = f"{JIRA_BASE_URL}/rest/api/2/search"
    params = {
        "jql": jql,
        "fields": "summary,status,issuetype"
    }

    response = requests.get(url, headers=HEADERS, params=params,
                            auth=HTTPBasicAuth(API_EMAIL, API_TOKEN))
    response.raise_for_status()
    return response.json()['issues']