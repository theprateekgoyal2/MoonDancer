from .apis import *

api_routes = [
    ('/api/triggers', manage_triggers_api, ['GET', 'POST', 'PUT', 'DELETE']),
    ('/api/triggers/fire', fire_api_trigger_api, ['GET']),
    ('/api/triggers/event/logs', get_event_logs_api, ['GET'])
]
