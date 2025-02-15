from .apis import *

api_routes = [
    ('/api/triggers', manage_triggers_api, ['GET', 'POST']),
    ('/api/triggers/fire', fire_api_trigger_api, ['GET'])
]
