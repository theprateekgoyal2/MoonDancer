import json
import logging
from typing import List
from redis_config import redis_client
from datetime import datetime, date, timedelta

from sql_config.utils import session_wrap
from .models import Triggers, EventLogs, ist_timezone
from .validations import validate_triggers_creation_payload, validate_params_to_fetch_triggers, \
    validate_trigger_update_payload
from .constants import TriggerType, ScheduledTriggerSubType, EventLogsStatus, CACHEKEYS


@session_wrap
def create_triggers_helper(payload: dict, session: any = None) -> dict:
    validation_result = validate_triggers_creation_payload(payload)
    if 'error' in validation_result:
        return validation_result

    trigger_type = payload.get('trigger_type')
    sub_type = payload.get('sub_type')
    schedule_date = payload.get('schedule_date')    # For one time
    schedule_time = payload.get('schedule_time')    # For daily recurring
    interval = payload.get('interval')  # For recurring interval
    api_payload = payload.get('api_payload')

    try:
        trigger = Triggers.create_trigger(trigger_type, sub_type, schedule_date, schedule_time, interval, api_payload)
        session.add(trigger)
        session.commit()

    except Exception as e:
        session.rollback()
        return {'error': f'An error occurred: {str(e)}'}

    return {
        'message': f'{trigger_type} Trigger created successfully',
        'Trigger_details': trigger.to_dict()
    }


@session_wrap
def get_triggers_helper(trigger_type: str, sub_type: str = None, session: any = None) -> dict:

    validation_result = validate_params_to_fetch_triggers(trigger_type, sub_type)
    if 'error' in validation_result:
        return validation_result

    query_results = get_triggers_based_on_trigger_type(session, trigger_type, sub_type)

    triggers_list = [trigger.to_dict() for trigger in query_results]

    response_data = {
        "message": "success",
        "total_triggers": len(triggers_list),
        "triggers": triggers_list
    }

    return response_data


@session_wrap
def fire_trigger_helper(trigger_id: int, session: any) -> dict:
    try:
        trigger = Triggers.get_by_id(session, trigger_id)
        if not trigger:
            return {"error": "Trigger not found"}

        EventLogs.create_event_log(trigger, session)
        print(f"{trigger.trigger_type} Trigger Fired: {trigger_id}")

        return {
            "message": f"Trigger {trigger_id} fired successfully!",
            "trigger_id": trigger_id,
            "payload": trigger.api_payload
        }

    except Exception as e:
        session.rollback()
        return {"error": str(e)}


@session_wrap
def get_event_logs(archived: bool, session: any) -> dict:
    """
    Fetch event logs from the last 2 hours by default, with an option to see archived logs.
    Uses caching to optimize frequent calls.
    """
    now = datetime.utcnow()
    two_hours_ago = now - timedelta(hours=2)

    cache_key = CACHEKEYS.ACTIVE.value
    if archived:
        cache_key = CACHEKEYS.ARCHIVED.value

    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Returning cached event logs!")
        return json.loads(cached_data)

    # Query logs from DB
    if archived:
        logs = session.query(EventLogs).filter(EventLogs.status == EventLogsStatus.ARCHIVED.value).all()
    else:
        logs = session.query(EventLogs).filter(EventLogs.dt_created >= two_hours_ago).all()

    logs_list = [{
        "id": log.prim_id,
        "trigger_id": log.trigger_id,
        "status": log.status,
        "trigger_type": log.trigger_type,
        "fired_at": str(log.fired_at),
        "api_payload": log.api_payload
    } for log in logs]

    response_data = {
        "message": "success",
        "total_logs": len(logs_list),
        "logs": logs_list
    }

    # Cache response for 5 minutes
    redis_client.setex(cache_key, 300, json.dumps(response_data))  # Cache for 300 sec (5 min)

    print("Data fetched from DB & cached.")
    return response_data


def get_triggers_based_on_trigger_type(session: any, trigger_type: str, sub_type: str = None) -> List[Triggers]:

    if trigger_type == TriggerType.API.value:
        query_results = (
            session.query(Triggers)
            .filter(Triggers.trigger_type == trigger_type)
            .order_by(Triggers.dt_created)
            .all()
        )

    else:
        query_results = (
            session.query(Triggers)
            .filter(
                Triggers.trigger_type == trigger_type,
                Triggers.sub_type == sub_type
            )
            .order_by(Triggers.dt_created)
            .all()
        )

    return query_results


@session_wrap
def update_triggers_helper(trigger_id: str, payload: dict, session: any) -> dict:
    trigger = Triggers.get_by_id(session, trigger_id)
    if not trigger:
        return {'error': f'No trigger found with this trigger_id: {trigger_id}'}

    validation_result = validate_trigger_update_payload(trigger, payload)
    if 'error' in validation_result:
        return validation_result

    sub_type = payload.get('sub_type')
    schedule_date = payload.get('schedule_date')
    schedule_time = payload.get('schedule_time')
    interval = payload.get('interval')
    api_payload = payload.get('api_payload')

    if interval:
        schedule_time = (datetime.now(ist_timezone) + timedelta(minutes=float(interval))).strftime("%H:%M:%S")

    trigger.sub_type = sub_type
    trigger.schedule_date = schedule_date
    trigger.schedule_time = schedule_time
    trigger.interval = interval
    trigger.api_payload = api_payload

    try:
        session.commit()
        logging.info(f"trigger with trigger_id: {trigger_id} updated")
        return {
            'message': 'Trigger Updated successfully',
            'Trigger_details': trigger.to_dict()
        }

    except Exception as e:
        session.rollback()
        return {'error': f'An error occurred: {str(e)}'}


@session_wrap
def delete_trigger_helper(trigger_id: str, session: any) -> dict:
    try:
        trigger = Triggers.get_by_id(session, trigger_id)
        if not trigger:
            return {'error': f'No trigger found with this trigger_id: {trigger_id}'}

        session.delete(trigger)
        session.commit()
        return {'message': 'Trigger deleted successfully!'}

    except Exception as e:
        session.rollback()
        return {'error': f'An error occurred: {str(e)}'}
