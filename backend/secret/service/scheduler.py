from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
from sqlalchemy import delete
from sqlalchemy.orm import Session
from secret.models import SecretModel
from infrastructure.database import SessionLocal

# Настройка планировщика
scheduler = BackgroundScheduler()

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

def start_scheduler():
    """
    Запустить планировщик (вызывается при старте приложения)
    """
    if not scheduler.running:
        scheduler.start()