from redis import Redis

from secret.schemas import SecretCreateSchema

class SecretCacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    def set_secret(self, access_key: str, secret: SecretCreateSchema) -> None:
        with self.redis as redis:
            if secret.ttl_seconds > 60:
                redis.setex(
                    name=access_key, 
                    time=60, 
                    value=secret.secret
                )
            else:
                redis.setex(
                    name=access_key, 
                    time=secret.ttl_seconds, 
                    value=secret.secret
                )

    def get_secret_by_access_key(self, access_key: str) -> str | None:
        with self.redis as redis:
            if cached_secret := redis.get(name=access_key):
                return cached_secret.decode('utf-8')
            
    def delete_secret_by_access_key(self, access_key: str):
        with self.redis as redis:
            redis.delete(access_key)