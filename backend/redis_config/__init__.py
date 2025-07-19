import redis
import logging
from common.env import REDIS_USER, REDIS_PASSWORD

redis_client = redis.Redis(
    host='redis-10909.c212.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=10909,
    decode_responses=True,
    username=REDIS_USER,
    password=REDIS_PASSWORD,
)

logging.info("✅ Redis Client Configured")
