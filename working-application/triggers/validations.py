from .constants import TriggerType


def validate_triggers_creation_payload(data: dict) -> dict:

    trigger_type = data.get('trigger_type')

    if trigger_type not in [TriggerType.SCHEDULED.value, TriggerType.API.value]:
        return {"error": "Invalid trigger type"}

    if trigger_type == TriggerType.SCHEDULED.value:
        schedule_time = data.get('schedule_time')
        schedule_date = data.get('schedule_date')
        interval = data.get('interval')

        # bool(x) converts each value to True if it has a valid value (not None or False).
        if sum(bool(x) for x in [schedule_time, schedule_date, interval]) != 1:
            return {"error": "Only one of schedule_time, schedule_date, or interval should be provided"}

    elif trigger_type == TriggerType.API.value and 'api_payload' not in data:
        return {"error": "API payload required for API trigger"}

    return {'message': 'success'}
