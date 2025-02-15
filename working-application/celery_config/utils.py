import pytz
import logging
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from sqlalchemy.exc import SQLAlchemyError
from sql_config import session_wrap
from triggers.models import Triggers, EventLogs
from triggers.constants import EventLogsStatus


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
        one_time_triggers = session.query(Triggers).filter(
            Triggers.trigger_type == 'scheduled',
            func.date(Triggers.schedule_date) == today,
            extract('hour', Triggers.schedule_date) == now.hour,
            extract('minute', Triggers.schedule_date) == now.minute
        ).all()

        for trigger in one_time_triggers:
            EventLogs.create_event_log(trigger, session)
            print(f"🔥 One-time Scheduled Trigger Fired: {trigger.prim_id} at {now}")

        # 2. Process Recurring Daily Triggers & Interval-Based Triggers
        daily_triggers = session.query(Triggers).filter(
            Triggers.trigger_type == 'scheduled',
            Triggers.schedule_date.is_(None),  # Recurring daily
            extract('hour', Triggers.schedule_time) == now.hour,
            extract('minute', Triggers.schedule_time) == now.minute
        ).all()

        for trigger in daily_triggers:
            EventLogs.create_event_log(trigger, session)
            print(f"🔥 Recurring Daily Trigger Fired: {trigger.prim_id} at {now}")

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
def update_event_states(session):
    """
    Updates event logs:
    - Archives logs created in the last 2 hours.
    - Deletes logs updated in the last 46 hours.
    """
    logging.info("this is scheduled task for updating event logs states")
    try:
        now = datetime.now(ist_timezone)
        two_hours_ago = now - timedelta(hours=2)
        forty_eight_hours_ago = now - timedelta(hours=48)

        # Fetch logs
        new_created_logs = session.query(EventLogs).filter(EventLogs.dt_created <= two_hours_ago, EventLogs.status == 'active').all()
        updated_logs = session.query(EventLogs).filter(EventLogs.dt_created <= forty_eight_hours_ago, EventLogs.status == 'archived').all()

        # Archive recent logs
        for log in new_created_logs:
            log.status = EventLogsStatus.ARCHIVED.value

        # Delete outdated logs
        for log in updated_logs:
            session.delete(log)

        session.commit()
        logging.info(f"{len(new_created_logs)} logs archived, {len(updated_logs)} logs deleted.")

    except SQLAlchemyError as e:
        session.rollback()
        logging.info(f"Database error: {e}")

    except Exception as e:
        session.rollback()
        logging.info(f"Unexpected error: {e}")
