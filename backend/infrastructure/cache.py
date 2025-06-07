from redis import Redis

redis_conn = Redis(host='localhost', port=6379, db=0)


def get_redis_connection() -> Redis:
    return redis_conn