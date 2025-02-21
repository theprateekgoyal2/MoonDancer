from enum import Enum


class TriggerType(Enum):
    SCHEDULED = 'scheduled'
    API = 'api'


class ScheduledTriggerSubType(Enum):
    DAILY = 'daily'
    FIXED_INTERVAL = 'fixed_interval'
    ONE_TIME = 'one_time'


class EventLogsStatus(Enum):
    ACTIVE = 'active'
    ARCHIVED = 'archived'
    DELETE = 'delete'


class CACHEKEYS(Enum):
    ACTIVE = 'event_logs_recent'
    ARCHIVED = 'event_logs_archived'


SUB_TYPE_ALLOWED_FIELDS = {
    ScheduledTriggerSubType.DAILY.value: {'schedule_time'},
    ScheduledTriggerSubType.ONE_TIME.value: {'schedule_date'},
    ScheduledTriggerSubType.FIXED_INTERVAL.value: {'interval'}
}
