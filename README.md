# MoonDancer

## Run Celery Worker
`celery -A celery_config.celery_worker worker --loglevel=info`


## Run Celery Beat
`celery -A celery_config.celery_worker beat --loglevel=info`

