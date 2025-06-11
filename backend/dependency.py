from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from infrastructure.database import get_db
from infrastructure.cache import get_redis_connection
from secret.repository.postgres import SecretRepository
from secret.repository.cache import SecretCacheRepository
from secret.service.service import SecretService

async def secret_repository_dep(db_session: AsyncSession = Depends(get_db)):
    return SecretRepository(db_session)

async def secret_cache_repository_dep(redis_conn: Redis = Depends(get_redis_connection)):
    return SecretCacheRepository(redis=redis_conn)

async def secret_service_dep(
    postgres_repo: SecretRepository = Depends(secret_repository_dep),
    cache_repo: SecretCacheRepository = Depends(secret_cache_repository_dep)
):
    return SecretService(secret_repository=postgres_repo, secret_cache_repository=cache_repo)
