from celery import Celery

# Initiates Celery and instructs it to use redis for queue
celery = Celery('celery_worker', broker='redis://localhost:6379/0')
