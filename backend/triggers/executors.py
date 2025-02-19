import pytz
import logging
from typing import List
from datetime import datetime, timedelta, date
from sqlalchemy import extract, func
from sqlalchemy.exc import SQLAlchemyError
from sql_config.utils import session_wrap
from .models import Triggers, EventLogs
from .constants import TriggerType, EventLogsStatus, CACHEKEYS


ist_timezone = pytz.timezone('Asia/Kolkata')


@session_wrap
def execute_scheduled_triggers(session):
    """
    Segregate scheduled triggers and execute them in order:
    1. One-time triggers (schedule_date == today)
    2. Recurring daily triggers & Interval-based triggers (set schedule_time = now + interval the first time)
    """
    logging.info("this is scheduled task for scheduled triggers")

    try:
        now = datetime.now(ist_timezone)
        today = now.date()

        # 1. Process One-Time Scheduled Triggers
        one_time_triggers = get_one_time_triggers(today, now, session)

        # 2. Process Recurring Daily Triggers & Interval-Based Triggers
        recurring_triggers = get_recurring_triggers(now, session)

        resultant_triggers = one_time_triggers + recurring_triggers

        for trigger in resultant_triggers:
            EventLogs.create_event_log(trigger, session)

            if trigger.schedule_date:
                print(f"One-time Scheduled Trigger Fired: {trigger.prim_id} at {now}")

            else:
                print(f"Recurring Trigger Fired: {trigger.prim_id} at {now}")
                if trigger.interval:
                    # Reset schedule_time for the next execution
                    trigger.schedule_time = (now + timedelta(minutes=float(trigger.interval))).strftime("%H:%M:%S")

        session.commit()
        logging.info("changes commited successfully")

    except SQLAlchemyError as e:
        session.rollback()
        logging.info(f"Database error: {e}")

    except Exception as e:
        session.rollback()
        logging.info(f"Unexpected error: {e}")


@session_wrap
def update_event_states(session: any):
    """
    Updates event logs:
    - Moves records older than 2 hours but less than 48 hours to 'archived'.
    - Moves records older than 48 hours to 'delete'.
    """
    logging.info("this is scheduled task for updating event logs states")
    try:
        now = datetime.utcnow()
        two_hours_ago = now - timedelta(hours=2)
        forty_eight_hours_ago = now - timedelta(hours=48)

        archived_state_logs = 0
        delete_state_logs = 0

        # Fetch all records older than 2 hours
        logs = session.query(EventLogs).filter(
            EventLogs.dt_created <= two_hours_ago
        ).all()

        # Process records based on age
        for log in logs:
            if forty_eight_hours_ago < log.dt_created <= two_hours_ago:
                log.status = EventLogsStatus.ARCHIVED.value  # Move to archived
                archived_state_logs += 1

            elif log.dt_created <= forty_eight_hours_ago:
                log.status = EventLogsStatus.DELETE.value  # Move to delete state
                delete_state_logs += 1

        # Commit the changes
        session.commit()
        print(f"Processed {len(logs)} records: {archived_state_logs} logs are moved to archived state "
              f"and {delete_state_logs} logs are moved to delete state.")

    except SQLAlchemyError as e:
        session.rollback()
        logging.info(f"Database error: {e}")

    except Exception as e:
        session.rollback()
        logging.info(f"Unexpected error: {e}")


def get_one_time_triggers(today: date, now: datetime, session: any) -> List[Triggers]:

    one_time_triggers = session.query(Triggers).filter(
        Triggers.trigger_type == TriggerType.SCHEDULED.value,
        func.date(Triggers.schedule_date) == today,
        extract('hour', Triggers.schedule_date) == now.hour,
        extract('minute', Triggers.schedule_date) == now.minute
    ).all()

    return one_time_triggers


def get_recurring_triggers(now: datetime, session: any) -> List[Triggers]:

    recurring_triggers = session.query(Triggers).filter(
        Triggers.trigger_type == TriggerType.SCHEDULED.value,
        Triggers.schedule_date.is_(None),  # Recurring daily
        extract('hour', Triggers.schedule_time) == now.hour,
        extract('minute', Triggers.schedule_time) == now.minute
    ).all()

    return recurring_triggers


@session_wrap
def delete_events(session: any):
    logging.info("this is scheduled task for deleting event logs")
    try:
        logs = session.query(EventLogs).filter(EventLogs.status == 'delete').all()
        for log in logs:
            session.delete(log)

        session.commit()
        print(f"{len(logs)}: logs are deleted")

    except SQLAlchemyError as e:
        session.rollback()
        logging.info(f"Database error: {e}")

    except Exception as e:
        session.rollback()
        logging.info(f"Unexpected error: {e}")
