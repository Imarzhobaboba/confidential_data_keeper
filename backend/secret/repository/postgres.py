from sqlalchemy import text, select, insert, delete, func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from infrastructure.models import SecretModel
from secret.schemas import SecretSchema, SecretCreateSchema

class SecretRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def ping_db(self) -> None:
        with self.db_session as session:
            try: 
                session.execute(text("SELECT 1"))    
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database is not available")
            return {"data": "db is working"}
        
    def get_secrets(self) -> list[SecretSchema]:
        query = select(SecretModel)
        with self.db_session as session:
            secrets: list[SecretSchema] = session.execute(query).scalars().all()
        return secrets

    def get_secret_by_access_key(self, access_key: str) -> str | None:
        query = (
            select(SecretModel)
            .where(access_key == SecretModel.access_key)
        )
        with self.db_session as session:
            if secret_schema := session.execute(query).scalar_one_or_none():
                return secret_schema.secret
    
    def create_secret(self, body: SecretCreateSchema, access_key) -> None:
        query = (
            insert(SecretModel)
            .values(
                secret=body.secret, 
                access_key = access_key,
                expires_at=func.now() + text(f"interval '{body.ttl_seconds} seconds'"),
            )
        )
        with self.db_session as session:
            session.execute(query)
            session.commit()
        

    def delete_secret(self, access_key: str) -> None:
        query = delete(SecretModel).where(SecretModel.access_key == access_key)
        with self.db_session as session:
            session.execute(query)
            session.commit()
