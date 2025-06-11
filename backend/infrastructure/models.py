from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import func, String, text
from datetime import datetime
from typing import Optional

from infrastructure.database import engine

class Base(DeclarativeBase):
    id: any
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

class SecretModel(Base):
    __tablename__ = 'secrets'

    access_key: Mapped[str] = mapped_column(primary_key=True)
    secret: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    expires_at: Mapped[datetime]

class RequestLog(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ip: Mapped[str] = mapped_column(String(45))
    method: Mapped[str] = mapped_column(String(10))
    path: Mapped[str]
    status_code: Mapped[int]
    timestamp: Mapped[datetime] = mapped_column(default=func.now())

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Вызов при старте приложения
# await create_tables()