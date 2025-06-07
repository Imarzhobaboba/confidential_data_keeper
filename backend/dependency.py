from fastapi import Depends
from sqlalchemy.orm import Session
from redis import Redis

from infrastructure.database import get_db
from infrastructure.cache import get_redis_connection
from secret.repository.postgres import SecretRepository
from secret.repository.cache import SecretCacheRepository
from secret.service.service import SecretService



def secret_repository_dep(db_session: Session = Depends(get_db)):
    return SecretRepository(db_session)

def secret_cache_repository_dep(redis_conn: Redis = Depends(get_redis_connection)):
    return SecretCacheRepository(redis=redis_conn)


def secret_service_dep(
    postgres_repo: SecretRepository = Depends(secret_repository_dep),
    cache_repo: SecretCacheRepository = Depends(secret_cache_repository_dep)):
    return SecretService(secret_repository=postgres_repo, secret_cache_repository=cache_repo)