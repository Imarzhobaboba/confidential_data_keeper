from redis.asyncio import Redis
from secret.schemas import SecretCreateSchema

class SecretCacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_secret(self, access_key: str, secret: str) -> None:
        await self.redis.setex(
            name=access_key, 
            time=30, 
            value=secret
        )

    async def get_secret_by_access_key(self, access_key: str) -> str | None:
        if cached_secret := await self.redis.get(name=access_key):
            return cached_secret.decode('utf-8')
        return None
            
    async def update_value_and_refresh(self, access_key: str, new_secret: str) -> None:
        async with self.redis.pipeline(transaction=True) as pipe:
            await pipe.set(name=access_key, value=new_secret, ex=30).execute()
            
    async def delete_secret_by_access_key(self, access_key: str) -> None:
        await self.redis.delete(access_key)
            
    async def refresh_ttl(self, access_key: str) -> None:
        await self.redis.expire(name=access_key, time=30)
