from flask import request
from .utils import create_triggers_helper, get_triggers_helper, fire_trigger_helper, \
    get_event_logs, update_triggers_helper, delete_trigger_helper


def manage_triggers_api():

    if request.method == 'GET':
        trigger_type = request.args.get('trigger_type')
        sub_type = request.args.get('sub_type')

        return get_triggers_helper(trigger_type, sub_type)

    if request.method == 'POST':
        payload = request.get_json()
        if not payload:
            return {'error': 'payload needed to create triggers'}

        return create_triggers_helper(payload)

    if request.method == 'PUT':
        trigger_id = request.args.get('trigger_id')
        payload = request.get_json()

        if not trigger_id:
            return {'error': 'No trigger_id provided'}

        if not payload:
            return {'error': 'payload needed to update triggers'}

        return update_triggers_helper(trigger_id, payload)

    if request.method == 'DELETE':
        trigger_id = request.args.get('trigger_id')
        if not trigger_id:
            return {'error': 'No trigger_id provided'}

        return delete_trigger_helper(trigger_id)


def fire_api_trigger_api():
    trigger_id = request.args.get('trigger_id')
    if not trigger_id:
        return {'error': 'Trigger id needed to fire a trigger'}

    return fire_trigger_helper(trigger_id)


def get_event_logs_api():
    archived = False

    if request.args.get("archived") == "true":
        archived = True

    return get_event_logs(archived)
