from sql_config.utils import session_wrap
from .models import Triggers
from .validations import validate_triggers_creation_payload


@session_wrap
def create_triggers_helper(payload: dict, session: any = None) -> dict:
    validation_result = validate_triggers_creation_payload(payload)
    if 'error' in validation_result:
        return validation_result

    trigger_type = payload.get('trigger_type')
    schedule_date = payload.get('schedule_date')    # For one time
    schedule_time = payload.get('schedule_time')    # For daily recurring
    interval = payload.get('interval')  # For recurring interval
    api_payload = payload.get('api_payload')

    try:
        trigger = Triggers.create_trigger(trigger_type, schedule_date, schedule_time, interval, api_payload)
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
def get_triggers_helper(trigger_id: int = None, session: any = None) -> dict:
    if not trigger_id:
        query_results = session.query(Triggers).order_by(Triggers.dt_created).all()
        return {
            'triggers': [trigger.to_dict() for trigger in query_results]
        }

    return Triggers.get_by_id(session, trigger_id).to_dict()


@session_wrap
def fire_trigger_helper(trigger_id: int, session: any) -> dict:
    try:
        trigger = Triggers.get_by_id(session, trigger_id)
        if not trigger:
            return {"error": "Trigger not found"}

        print(f"{trigger.trigger_type} Trigger Fired: {trigger_id}")

        return {
            "message": f"API Trigger {trigger_id} fired successfully!",
            "trigger_id": trigger_id,
            "payload": trigger.api_payload
        }

    except Exception as e:
        session.rollback()
        return {"error": str(e)}
