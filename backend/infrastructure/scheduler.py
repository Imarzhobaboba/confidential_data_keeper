from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from infrastructure.models import SecretModel
from infrastructure.database import SessionLocal
from config import settings

# Настройка планировщика
jobstores = {
    'default': SQLAlchemyJobStore(url=settings.DATABASE_URL)
}

scheduler = BackgroundScheduler(jobstores=jobstores)

def delete_secret_job(access_key: str):
    """
    Задача для удаления секрета по истечении времени
    """
    db = SessionLocal()
    try:
        query = delete(SecretModel).where(SecretModel.access_key == access_key)
        db.execute(query)
        db.commit()
    except Exception as e:
        # Логирование ошибки, если необходимо
        print(f"Error deleting secret {access_key}: {e}")
        db.rollback()
    finally:
        db.close()

def schedule_secret_deletion(access_key: str, ttl_seconds: int):
    """
    Запланировать удаление секрета через указанное количество секунд
    """
    scheduler.add_job(
        delete_secret_job,
        'date',
        run_date=datetime.now() + timedelta(seconds=ttl_seconds),
        args=[access_key],
        id=f"delete_secret_{access_key}",
        misfire_grace_time=3600,
        replace_existing=True
    )

def cleanup_expired_secrets():
    """Очистка просроченных секретов при запуске"""
    db = SessionLocal()
    try:
        # Удаляем все просроченные секреты
        expired_query = delete(SecretModel).where(
            SecretModel.expires_at <= datetime.now()
        )
        db.execute(expired_query)
        
        # Перепланируем активные секреты
        active_secrets = db.execute(
            select(SecretModel.access_key, SecretModel.expires_at)
            .where(SecretModel.expires_at > datetime.now())
        ).all()
        
        for access_key, expires_at in active_secrets:
            schedule_secret_deletion(access_key, expires_at)
            
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    """
    Запустить планировщик (вызывается при старте приложения)
    """
    if not scheduler.running:
        cleanup_expired_secrets()
        scheduler.start()
