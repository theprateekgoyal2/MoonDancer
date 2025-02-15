from celery import Celery

celery = Celery('celery_worker', broker='redis://localhost:6379/0')
