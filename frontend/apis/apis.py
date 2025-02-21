import requests

BASE_URL = "http://localhost:5000"


def fetch_event_logs(archived=False) -> dict:
    """
    Fetch recent or archived event logs from the API.
    """
    endpoint = "/api/triggers/event/logs"
    if archived:
        endpoint += "?archived=true"

    response = requests.get(BASE_URL + endpoint)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch logs"}


def fetch_triggers(trigger_type: str, sub_type: str = None) -> dict:
    """
    Fetch all triggers from the API.
    """
    endpoint = f"/api/triggers?trigger_type={trigger_type}"
    if sub_type:
        endpoint += f"&sub_type={sub_type}"

    response = requests.get(BASE_URL + endpoint)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch triggers"}


def create_triggers(payload: dict) -> dict:
    endpoint = "/api/triggers"

    url = BASE_URL + endpoint

    response = requests.post(url, json=payload)
    return response.json() if response.status_code == 200 else {"error": "Failed to create trigger"}


def update_trigger(trigger_id: str, payload: dict) -> dict:
    endpoint = f"/api/triggers?trigger_id={trigger_id}"

    url = BASE_URL + endpoint
    response = requests.put(url, json=payload)
    return response.json() if response.status_code == 200 else {"error": "Failed to edit trigger"}


def delete_trigger(trigger_id: str) -> dict:
    endpoint = f"/api/triggers?trigger_id={trigger_id}"

    url = BASE_URL + endpoint
    response = requests.delete(url)
    return response.json() if response.status_code == 200 else {"error": "Failed to delete trigger"}
