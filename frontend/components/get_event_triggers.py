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

    trigger_list = triggers.get("triggers", [])

    if not trigger_list:
        st.write("No triggers found.")
        return

    # Define table headers
    headers = list(trigger_list[0].keys()) + ["Actions"]

    # Create table layout
    cols = st.columns(len(headers))

    # Render headers
    for col, header in zip(cols, headers):
        col.write(f"**{header}**")

    # Render table rows
    for row in trigger_list:
        cols = st.columns(len(headers))

        for col, key in zip(cols[:-1], headers[:-1]):  # Fill data columns
            col.write(row.get(key, "N/A"))

        trigger_id = row["trigger_id"]

        # Action Buttons
        with cols[-1]:
            edit_clicked = st.button("✏️ Edit", key=f"edit_{trigger_id}")
            delete_clicked = st.button("❌ Delete", key=f"delete_{trigger_id}")

            if edit_clicked:
                enter_edit_mode(trigger_id, row)

            if delete_clicked:
                delete_trigger_and_refresh(trigger_id)


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
