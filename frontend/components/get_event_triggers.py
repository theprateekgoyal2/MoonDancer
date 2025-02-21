import pandas as pd
import streamlit as st
from .constants import TriggerTypeValue, SubTypeValue
from .update_trigger import show_edit_screen
from frontend.apis.apis import fetch_triggers, delete_trigger


def show_event_triggers():
    """
    Main function to display the Event Triggers Dashboard.
    """

    if is_editing_trigger():
        show_edit_screen(st.session_state.editing_trigger_id, st.session_state.trigger_obj)
        return

    initialize_session_state()

    st.title("📜 Event Triggers Dashboard")

    trigger_options = select_trigger_options()

    trigger_type = trigger_options.get('trigger_type')
    sub_type = trigger_options.get('sub_type')

    if not trigger_type:
        st.write("No option selected")
        return

    display_triggers(trigger_type, sub_type)


def is_editing_trigger():
    """
    Check if an editing trigger session state exists.
    """

    return "editing_trigger_id" in st.session_state and st.session_state.editing_trigger_id


def initialize_session_state():
    """
    Initialize session state variables if not already set.
    """
    if "refresh_triggers" not in st.session_state:
        st.session_state.refresh_triggers = False


def select_trigger_options() -> dict:
    """
    Allow users to select trigger type and sub_type (if applicable).
    """

    trigger_type = st.radio("Select Trigger Type:", ["Scheduled", "API Based"], index=None)
    sub_type = None

    if trigger_type == "Scheduled":
        sub_type = st.radio("Select Scheduled Trigger Type:", ["Daily", "Fixed Interval", "One time"], index=0)
        sub_type = SubTypeValue.get(sub_type)

    trigger_options = {'trigger_type': trigger_type, 'sub_type': sub_type}

    return trigger_options


def display_triggers(trigger_type: str, sub_type: str):
    """
    Fetch and display event triggers in a table with action buttons.
    """
    triggers = fetch_triggers(TriggerTypeValue.get(trigger_type), sub_type)
    st.session_state.refresh_triggers = False

    if "error" in triggers:
        st.error(triggers["error"])
        return

    st.write(f"✅ Found {triggers['total_triggers']} triggers")

    df = pd.DataFrame(triggers.get('triggers'))
    apply_table_styling()

    for _, row in df.iterrows():
        display_trigger_row(row)


def apply_table_styling():
    """
    Apply CSS styling for table headers.
    """
    st.markdown(
        """
        <style>
            th { 
                min-width: 100px !important;  
                white-space: nowrap;  
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def display_trigger_row(row: any):
    """
    Display a row with data and action buttons.
    """

    col1, col2, col3 = st.columns([5, 1, 1])

    with col1:
        st.dataframe(pd.DataFrame([row]), hide_index=True)

    trigger_id = row.at["trigger_id"]

    with col2:
        if st.button("✏️ Edit", key=f"edit_{trigger_id}"):
            enter_edit_mode(trigger_id, row)

    with col3:
        if st.button("❌ Delete", key=f"delete_{trigger_id}"):
            delete_trigger_and_refresh(trigger_id)


def enter_edit_mode(trigger_id: str, row: any):
    """
    Set session state to edit mode and refresh the page.
    """

    st.session_state.editing_trigger_id = trigger_id
    st.session_state.trigger_obj = row
    st.rerun()


def delete_trigger_and_refresh(trigger_id: str):
    """
    Delete a trigger and refresh the page.
    """

    delete_trigger(trigger_id)
    st.write("✅ Event Trigger deleted")
    st.session_state.refresh_triggers = True
    st.rerun()
