import streamlit as st
import requests

# Backend API base URL
BASE_URL = "http://localhost:5000"  # Change to your deployed URL if needed

st.title("📜 Event Logs Dashboard")

# Fetch logs
option = st.radio("Select Log Type:", ["Recent (Last 2 Hours)", "Archived"])
endpoint = "/api/triggers/event/logs"
if option == "Archived":
    endpoint += "?archived=true"

if st.button("Fetch Logs"):
    response = requests.get(BASE_URL + endpoint)

    if response.status_code == 200:
        data = response.json()
        st.write(f"✅ Found {data['total_logs']} logs")

        # Display logs in table format
        if data["logs"]:
            st.table(data["logs"])
        else:
            st.warning("No logs found.")
    else:
        st.error("Failed to fetch logs. Check the backend.")
