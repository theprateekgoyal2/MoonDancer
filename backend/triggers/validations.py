from .models import Triggers
from .constants import TriggerType, ScheduledTriggerSubType, SUB_TYPE_ALLOWED_FIELDS


def validate_triggers_creation_payload(data: dict) -> dict:

    trigger_type = data.get('trigger_type')
    sub_type = data.get('sub_type')

    if trigger_type not in [TriggerType.SCHEDULED.value, TriggerType.API.value]:
        return {"error": "Invalid trigger type"}

    if trigger_type == TriggerType.SCHEDULED.value:
        schedule_time = data.get('schedule_time')
        schedule_date = data.get('schedule_date')
        interval = data.get('interval')

        if not sub_type or sub_type not in SUB_TYPE_ALLOWED_FIELDS:
            return {"error": "sub type missing or invalid sub type"}

        # Check which fields are provided
        provided_fields = {k for k, v in {
            "schedule_time": schedule_time,
            "schedule_date": schedule_date,
            "interval": interval
        }.items() if v is not None}

        # Validate that only the allowed field for the given sub_type is provided
        if provided_fields != SUB_TYPE_ALLOWED_FIELDS[sub_type]:
            return {"error": f"Invalid fields for sub_type '{sub_type}'. Allowed: {SUB_TYPE_ALLOWED_FIELDS[sub_type]}"}

    if trigger_type == TriggerType.API.value and sub_type:
        return {"error": "sub type not available for API Based Trigger"}

    elif trigger_type == TriggerType.API.value and 'api_payload' not in data:
        return {"error": "API payload required for API trigger"}

    return {'message': 'success'}


def validate_params_to_fetch_triggers(trigger_type: str, sub_type: str = None) -> dict:

    if trigger_type not in [TriggerType.SCHEDULED.value, TriggerType.API.value]:
        return {"error": "Invalid trigger type"}

    if trigger_type == TriggerType.SCHEDULED.value:
        if not sub_type or sub_type not in SUB_TYPE_ALLOWED_FIELDS:
            return {"error": "sub type missing or invalid sub type"}

    return {'message': 'success'}


def validate_trigger_update_payload(trigger: Triggers, payload: dict) -> dict:

    trigger_type = trigger.trigger_type

    sub_type = payload.get('trigger_sub_type')
    schedule_date = payload.get('schedule_date')
    schedule_time = payload.get('schedule_time')
    interval = payload.get('interval')
    api_payload = payload.get('api_payload')

    if trigger_type == TriggerType.API.value and (sub_type or schedule_date or schedule_time or interval):
        return {"error": "For API Based triggers only api_payload can be edited"}

    if trigger_type == TriggerType.SCHEDULED.value and api_payload:
        return {"error": "For scheduled triggers api payload can't be added"}

    if sub_type not in SUB_TYPE_ALLOWED_FIELDS:
        return {"error": "invalid sub type provided"}

    # Check which fields are provided
    provided_fields = {k for k, v in {
        "schedule_date": schedule_date,
        "schedule_time": schedule_time,
        "interval": interval
    }.items() if v is not None}

    # Validate that only the allowed field for the given sub_type is provided
    if provided_fields != SUB_TYPE_ALLOWED_FIELDS[sub_type]:
        return {"error": f"Invalid fields for sub_type '{sub_type}'. Allowed: {SUB_TYPE_ALLOWED_FIELDS[sub_type]}"}

    return {'message': 'success'}
