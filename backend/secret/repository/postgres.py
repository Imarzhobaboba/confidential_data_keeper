from sqlalchemy import text, select, insert, delete, update, func
from sqlalchemy.orm import Session

from infrastructure.models import SecretModel
from secret.schemas import SecretSchema, SecretCreateSchema, SecretUpdateSchema

class SecretRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_secret(self, access_key: str) -> SecretSchema | None:
        query = (
            select(SecretModel)
            .where(access_key == SecretModel.access_key)
        )
        with self.db_session as session:
            if result := session.execute(query).scalar_one_or_none():
                return result
    
    def create_secret(self, body: SecretCreateSchema, access_key: str) -> SecretSchema | None:
        query = (
            insert(SecretModel)
            .values(
                secret=body.secret, 
                access_key = access_key,
                expires_at=func.now() + text(f"interval '{body.ttl_seconds} seconds'"),
            )
            .returning(SecretModel)
        )
        with self.db_session as session:
            if result := session.execute(query).scalar_one_or_none():
                session.commit()
                return result
            
    def update_secret(self, access_key: str, secret: str) -> SecretSchema | None:
        query = (
            update(SecretModel)
            .where(SecretModel.access_key == access_key)
            .values(secret=secret)
            .returning(SecretModel)
        )
        with self.db_session as session:
            if result := session.execute(query).scalar_one_or_none():
                session.commit()
                return result
            
    def update_time(self, access_key: str, additional_ttl_seconds: int) -> SecretSchema | None:
        query = (
            update(SecretModel)
            .where(SecretModel.access_key == access_key)
            .values(expires_at=SecretModel.expires_at + text(f"interval '{additional_ttl_seconds} seconds'"))
            .returning(SecretModel)
        )
        with self.db_session as session:
            if result := session.execute(query).scalar_one_or_none():
                session.commit()
                return result 
        

    def delete_secret(self, access_key: str) -> SecretSchema | None:
        query = (
            delete(SecretModel)
            .where(SecretModel.access_key == access_key)
            .returning(SecretModel)
        )
        with self.db_session as session:
            if result := session.execute(query).scalar_one_or_none():
                session.commit()
                return result
