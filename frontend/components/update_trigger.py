import streamlit as st
from datetime import datetime, time, date
from .constants import TriggerTypeValue
from frontend.apis.apis import update_trigger


def show_edit_screen(trigger_id: str, trigger_details: any):
    """
    Main function to display the edit screen.
    """

    st.title("✏️ Edit Event Trigger")

    trigger_type = trigger_details.get('trigger_type')

    if trigger_type == TriggerTypeValue.get('Scheduled'):
        edited_data = handle_scheduled_trigger()
    else:
        edited_data = handle_api_trigger()

    show_action_buttons(trigger_id, edited_data)


def handle_scheduled_trigger() -> dict:
    """
    Handles scheduled trigger inputs.
    """

    new_trigger_sub_type = st.selectbox(
        "Select Trigger Sub Type:",
        ["Daily", "Fixed Interval", "One time"],
        index=None
    )

    new_schedule_time, new_schedule_date, new_interval = None, None, None

    if new_trigger_sub_type == "Daily":
        new_schedule_time = st.time_input("Select a time", value=time(0, 0), step=300)

    elif new_trigger_sub_type == "Fixed Interval":
        new_interval = st.text_input("Enter the time interval for trigger", placeholder="Enter the time interval..")

    elif new_trigger_sub_type == "One time":
        trigger_date = st.date_input("Select a date")
        trigger_time = st.time_input("Select a time", value=time(0, 0), step=300)

        if trigger_date and trigger_time:
            new_schedule_date = datetime.combine(trigger_date, trigger_time)
            st.write("Selected DateTime:", new_schedule_date)

    return {
        "trigger_sub_type": new_trigger_sub_type,
        "schedule_time": new_schedule_time,
        "schedule_date": new_schedule_date,
        "interval": float(new_interval) if new_interval else None
    }


def handle_api_trigger() -> dict:
    """
    Handles API-based trigger inputs.
    """

    new_api_payload = st.text_area("Enter JSON Payload", placeholder="Enter your payload here...")
    return {"api_payload": new_api_payload}


def show_action_buttons(trigger_id: str, edited_data: dict):
    """
    Displays save and cancel buttons.
    """

    if st.button("Save Changes"):
        update_result = update_trigger(trigger_id, edited_data)
        if "error" in update_result:
            st.error("Failed to update trigger")
        else:
            st.success("✅ Trigger updated successfully!")
            st.session_state.editing_trigger_id = None  # Reset edit state
            st.rerun()

    if st.button("Cancel"):
        st.session_state.editing_trigger_id = None
        st.rerun()
