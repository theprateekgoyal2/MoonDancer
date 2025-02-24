import redis
import logging
from common.env import REDIS_USER, REDIS_PASSWORD

redis_client = redis.Redis(
    host='redis-12220.c330.asia-south1-1.gce.redns.redis-cloud.com',
    port=12220,
    decode_responses=True,
    username=REDIS_USER,
    password=REDIS_PASSWORD,
)

logging.info("✅ Redis Client Configured")
