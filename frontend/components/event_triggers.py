import streamlit as st
from frontend.apis.apis import fetch_triggers


def show_event_triggers():
    st.title("📜 Event Triggers Dashboard")

    # Add a placeholder option
    option = st.radio("Select Trigger Type:", ["Scheduled", "API Based"])

    # Conditionally show option1 when "Scheduled" is selected
    option1 = None  # Default value

    if option == "Scheduled":
        option1 = st.radio("Select Scheduled Trigger Type:", ["Daily", "Fixed Interval", "One time"], index=None)

    # Fetch triggers from API
    triggers = fetch_triggers()

    if "error" in triggers:
        st.error(triggers["error"])
    else:
        st.write(f"✅ Found {triggers['total_triggers']} triggers")
        st.table(triggers["triggers"]) if triggers["triggers"] else st.warning("No triggers found.")

    # Debugging (optional)
    st.write(f"Trigger Type: {option or 'Not Selected'}")
    if option1:
        st.write(f"Scheduled Type: {option1}")
