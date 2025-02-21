import requests

BASE_URL = "http://localhost:5000"


def fetch_event_logs(archived=False):
    """Fetch recent or archived event logs from the API."""
    endpoint = "/api/triggers/event/logs"
    if archived:
        endpoint += "?archived=true"

    response = requests.get(BASE_URL + endpoint)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch logs"}


def fetch_triggers():
    """Fetch all triggers from the API."""
    endpoint = "/api/triggers"

    response = requests.get(BASE_URL + endpoint)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch triggers"}
