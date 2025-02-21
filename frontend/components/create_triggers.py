import json
import streamlit as st
from datetime import datetime, time
from .constants import TriggerTypeValue, SubTypeValue
from frontend.apis.apis import create_triggers


def initialize_session_state():
    """
    Initialize session state variables if not already set.
    """
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    if "placeholder" not in st.session_state:
        st.session_state.placeholder = "This is placeholder"


def handle_api_based_trigger(option: str):
    """
    Handles the input and submission for API-based triggers.
    """
    json_input = st.text_area("Enter JSON Payload", placeholder="Enter your payload here...")

    if st.button("Submit"):
        payload = {
            "trigger_type": TriggerTypeValue.get(option),
            "api_payload": json.loads(json_input)  # Store the JSON input
        }
        submit_trigger(payload)


def handle_scheduled_trigger():
    """
    Handles input selection for scheduled triggers.
    """
    option1 = st.radio("Select Scheduled Trigger Type:", ["Daily", "Fixed Interval", "One time"], index=None)

    time_selected, trigger_date, trigger_time, datetime_value, time_interval = None, None, None, None, None

    if option1 == "Daily":
        time_selected = st.time_input("Select a time", value=time(0, 0), step=300)

    elif option1 == "Fixed Interval":
        time_interval = st.text_input("Enter the time interval for trigger", placeholder="Enter the time interval..")

    elif option1 == "One time":
        trigger_date = st.date_input("Select a date")
        trigger_time = st.time_input("Select a time", value=time(0, 0), step=300)

        if trigger_date and trigger_time:
            datetime_value = datetime.combine(trigger_date, trigger_time)
            st.write("Selected DateTime:", datetime_value)

    return option1, time_selected, datetime_value, time_interval


def create_trigger_payload(option, option1, time_selected, datetime_value, time_interval):
    """
    Creates the payload for submitting an event trigger.
    """
    return {
        "trigger_type": TriggerTypeValue.get(option),
        "sub_type": SubTypeValue.get(option1),
        "schedule_date": str(datetime_value) if datetime_value else None,
        "schedule_time": str(time_selected) if time_selected else None,
        "interval": float(time_interval) if time_interval else None
    }


def submit_trigger(payload):
    """
    Handles trigger submission and response display.
    """
    creation_result = create_triggers(payload)
    if "error" in creation_result:
        st.error(creation_result["error"])
    else:
        st.write(f"✅ Event Trigger created: {creation_result.get('Trigger_details')}")


def create_event_triggers():
    """
    Main function to create event triggers.
    """
    st.title("📝 Create Events Triggers")

    # Initialize session state
    initialize_session_state()

    # Select trigger type
    option = st.radio("Select Trigger Type:", ["Scheduled", "API Based"], index=None)

    if option == "API Based":
        handle_api_based_trigger(option)
        return  # Stop further execution if API Based is selected

    # Handle scheduled triggers
    option1, time_selected, datetime_value, time_interval = handle_scheduled_trigger()

    if st.button("Submit"):
        payload = create_trigger_payload(option, option1, time_selected, datetime_value, time_interval)
        submit_trigger(payload)
