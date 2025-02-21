import streamlit as st
from frontend.apis.apis import fetch_event_logs


def show_event_logs():
    st.title("📜 Event Logs Dashboard")

    option = st.radio("Select Log Type:", ["Recent (Last 2 Hours)", "Archived"])
    logs = fetch_event_logs(archived=(option == "Archived"))

    if "error" in logs:
        st.error(logs["error"])
    else:
        st.write(f"✅ Found {logs['total_logs']} logs")
        st.table(logs["logs"]) if logs["logs"] else st.warning("No logs found.")
