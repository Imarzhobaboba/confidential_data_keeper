from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from datetime import datetime


class Base(DeclarativeBase):
    id: any
    __name__: str

    __allow_unmapped__ = str = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()



class SecretModel(Base):
    __tablename__ = 'secrets'

    access_key: Mapped[str] = mapped_column(primary_key=True)
    secret: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    expires_at: Mapped[datetime]
