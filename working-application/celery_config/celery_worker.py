import logging
from celery_config import celery
from celery.schedules import crontab
from triggers.utils import execute_scheduled_triggers, update_event_states, delete_events


@celery.task(name="celery_config.celery_worker.execute_scheduled_triggers_helper")
def execute_scheduled_triggers_helper():
    logging.info("Task `execute_scheduled_triggers_helper` is running!")
    execute_scheduled_triggers()
    logging.info("Task `execute_scheduled_triggers_helper` completed execution.")


@celery.task(name="celery_config.celery_worker.update_event_states_helper")
def update_event_states_helper():
    logging.info("Task `update_event_states_helper` is running!")
    update_event_states()
    logging.info("Task `update_event_states_helper` completed execution.")


@celery.task(name="celery_config.celery_worker.delete_events_helper")
def delete_events_helper():
    logging.info("Task `delete_events_helper` is running!")
    delete_events()
    logging.info("Task `delete_events_helper` completed execution.")


# Schedules the tasks, basically sends the tasks to redis-queue
celery.conf.beat_schedule = {
    'execute_scheduled_triggers_task': {
        'task': 'celery_config.celery_worker.execute_scheduled_triggers_helper',
        'schedule': 60.0
    },
    'update_event_states_task': {
        'task': 'celery_config.celery_worker.update_event_states_helper',
        'schedule': crontab(minute='*/30')  # Runs every 30 minutes
    },
    'delete_events_task': {
        'task': 'celery_config.celery_worker.delete_events_helper',
        'schedule': crontab(minute='*/30')
    }
}
