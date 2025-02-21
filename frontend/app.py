import os
import sys
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.event_logs import show_event_logs
from components.event_triggers import show_event_triggers

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["📜 Show Event Logs", "⏳ Show Event Triggers"],
    index=0  # Default selection
)

if page == "📜 Show Event Logs":
    show_event_logs()

if page == "⏳ Show Event Triggers":
    show_event_triggers()
