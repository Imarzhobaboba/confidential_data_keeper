from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool

from alembic import context

import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import settings
from infrastructure.models import *  # noqa

# Конфигурация Alembic
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,  # <- Добавляем фильтр
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn, 
                target_metadata=target_metadata,
                include_object=include_object,  # <- Добавляем фильтр
            )
        )
        async with connection.begin():
            await connection.run_sync(lambda sync_conn: context.run_migrations())

# Функция для исключения таблицы apscheduler_jobs
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name == "apscheduler_jobs":
        return False
    return True

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())