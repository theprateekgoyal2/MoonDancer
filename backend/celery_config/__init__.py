from celery import Celery
from common.env import REDIS_IP

# Initiates Celery and instructs it to use redis for queue
celery = Celery('celery_worker', broker=f'redis://{REDIS_IP}:6379/0')
