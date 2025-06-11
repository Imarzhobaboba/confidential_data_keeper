from sqlalchemy import select, insert, delete, update, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from infrastructure.models import SecretModel
from secret.schemas import SecretSchema, SecretCreateSchema

class SecretRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_secret(self, access_key: str) -> Optional[SecretSchema]:
        query = select(SecretModel).where(access_key == SecretModel.access_key)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()
    
    async def create_secret(self, body: SecretCreateSchema, access_key: str) -> Optional[SecretSchema]:
        query = (
            insert(SecretModel)
            .values(
                secret=body.secret,
                access_key=access_key,
                expires_at=func.now() + text(f"interval '{body.ttl_seconds} seconds'")
            )
            .returning(SecretModel)
        )
        
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.scalar_one_or_none()
            
    async def update_secret(self, access_key: str, secret: str) -> Optional[SecretSchema]:
        query = (
            update(SecretModel)
            .where(SecretModel.access_key == access_key)
            .values(secret=secret)
            .returning(SecretModel)
        )
        
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.scalar_one_or_none()
            
    async def update_time(self, access_key: str, additional_ttl_seconds: int) -> Optional[SecretSchema]:
        query = (
            update(SecretModel)
            .where(SecretModel.access_key == access_key)
            .values(expires_at=SecretModel.expires_at + text(f"interval '{additional_ttl_seconds} seconds'"))
            .returning(SecretModel)
        )
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.scalar_one_or_none()
        
    async def delete_secret(self, access_key: str) -> Optional[SecretSchema]:
        query = (
            delete(SecretModel)
            .where(SecretModel.access_key == access_key)
            .returning(SecretModel)
        )
        
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.scalar_one_or_none()
