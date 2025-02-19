from enum import Enum


class TriggerType(Enum):
    SCHEDULED = 'scheduled'
    API = 'api'


class EventLogsStatus(Enum):
    ACTIVE = 'active'
    ARCHIVED = 'archived'
    DELETE = 'delete'


class CACHEKEYS(Enum):
    ACTIVE = 'event_logs_recent'
    ARCHIVED = 'event_logs_archived'
