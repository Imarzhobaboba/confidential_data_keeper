from redis import Redis

from secret.schemas import SecretCreateSchema

class SecretCacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    def set_secret(self, access_key: str, secret: SecretCreateSchema) -> None:
        with self.redis as redis:
            if secret.ttl_seconds > 30:
                redis.setex(
                    name=access_key, 
                    time=30, 
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
            
    def update_value_and_refresh(self, access_key: str, new_secret: str) -> None:
        with self.redis as redis:
            redis.pipeline(transaction=True).set(name=access_key, value=new_secret, ex=30).execute()
            
    def delete_secret_by_access_key(self, access_key: str) -> None:
        with self.redis as redis:
            redis.delete(access_key)
            
    def refresh_ttl(self, access_key: str) -> None:
        self.redis.expire(name=access_key, time=30)