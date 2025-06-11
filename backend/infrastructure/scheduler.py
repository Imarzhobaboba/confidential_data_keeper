from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
from sqlalchemy import delete, select
from config import settings

from infrastructure.database import async_session
from infrastructure.models import SecretModel

# Используем синхронный URL для APScheduler
SYNC_DATABASE_URL = settings.DATABASE_URL.replace('postgresql+asyncpg', 'postgresql')

jobstores = {
    'default': SQLAlchemyJobStore(url=SYNC_DATABASE_URL)
}

scheduler = AsyncIOScheduler(jobstores=jobstores)

async def delete_secret_job(access_key: str):
    async with async_session() as db:
        try:
            query = delete(SecretModel).where(SecretModel.access_key == access_key)
            await db.execute(query)
            await db.commit()
            
            from infrastructure.cache import redis_conn
            from secret.repository.cache import SecretCacheRepository
            await SecretCacheRepository(redis=redis_conn).delete_secret_by_access_key(access_key=access_key)
        except Exception as e:
            await db.rollback()
            print(f"Error deleting secret {access_key}: {e}")

def schedule_secret_deletion(access_key: str, ttl_seconds: int):
    scheduler.add_job(
        delete_secret_job,
        'date',
        run_date=datetime.now() + timedelta(seconds=ttl_seconds),
        args=[access_key],
        id=f"delete_secret_{access_key}",
        misfire_grace_time=3600,
        replace_existing=True
    )
    
def update_schedule(access_key: str, additional_ttl_seconds: int):
    job_id = f"delete_secret_{access_key}"
    job = scheduler.get_job(job_id)
    if not job:
        raise ValueError(f"No scheduled deletion found for secret {access_key}")
    new_run_time = job.next_run_time + timedelta(seconds=additional_ttl_seconds)
    scheduler.reschedule_job(
        job_id,
        trigger='date',
        run_date=new_run_time
    )

async def cleanup_expired_secrets():
    async with async_session() as db:
        try:
            # Удаляем просроченные секреты
            expired_query = delete(SecretModel).where(
                SecretModel.expires_at <= datetime.now()
            )
            await db.execute(expired_query)
            
            # Перепланируем активные секреты
            active_secrets = (await db.execute(
                select(SecretModel.access_key, SecretModel.expires_at)
                .where(SecretModel.expires_at > datetime.now())
            )).all()
            
            for access_key, expires_at in active_secrets:
                ttl_seconds = (expires_at - datetime.now()).total_seconds()
                schedule_secret_deletion(access_key, int(ttl_seconds))
            
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise

def start_scheduler():
    if not scheduler.running:
        # Запускаем cleanup в event loop
        import asyncio
        asyncio.create_task(cleanup_expired_secrets())
        scheduler.start()
