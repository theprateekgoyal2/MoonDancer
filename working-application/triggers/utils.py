from sql_config.utils import session_wrap
from .models import Triggers
from .constants import TriggerType


@session_wrap
def manage_triggers(payload: dict, session: any) -> dict:
    validation_result = validate_triggers_creation_payload(payload)
    if 'error' in validation_result:
        return validation_result

    trigger_type = payload.get('trigger_type')
    schedule_time = payload.get('schedule_time')
    api_payload = payload.get('api_payload')

    try:
        trigger = Triggers.create_trigger(trigger_type, schedule_time, api_payload)
        session.add(trigger)
        session.commit()
    except Exception as e:
        session.rollback()
        return {'error': f'An error occurred: {str(e)}'}

    return trigger.to_dict()


def validate_triggers_creation_payload(data: dict) -> dict:

    if 'trigger_type' not in data or data['trigger_type'] not in [TriggerType.SCHEDULED.value, TriggerType.API.value]:
        return {"error": "Invalid trigger type"}

    if data['trigger_type'] == TriggerType.SCHEDULED.value and 'schedule_time' not in data:
        return {"error": "Schedule time required for scheduled trigger"}

    elif data['trigger_type'] == TriggerType.API.value and 'api_payload' not in data:
        return {"error": "API payload required for API trigger"}

    return {'message': 'success'}
