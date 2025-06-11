from redis.asyncio import Redis
from config import settings

redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def get_redis_connection() -> Redis:
    return redis_conn
