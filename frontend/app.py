import os
import sys
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.get_event_logs import show_event_logs
from components.get_event_triggers import show_event_triggers
from components.create_triggers import create_event_triggers

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["⏳ Show Event Triggers", "📝 Create Event Triggers", "📜 Show Event Logs"],
    index=0  # Default selection
)

if page == "📝 Create Event Triggers":
    create_event_triggers()

if page == "⏳ Show Event Triggers":
    show_event_triggers()

if page == "📜 Show Event Logs":
    show_event_logs()
