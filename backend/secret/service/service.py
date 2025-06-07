from fastapi import HTTPException

from dataclasses import dataclass
from uuid import uuid4

from secret.repository.postgres import SecretRepository
from secret.repository.cache import SecretCacheRepository
from secret.schemas import SecretSchema, SecretCreateSchema

from secret.service.crypto import encrypt, decrypt
from infrastructure.scheduler import scheduler, schedule_secret_deletion


@dataclass
class SecretService:
    secret_repository: SecretRepository
    secret_cache_repository: SecretCacheRepository

    def get_secrets(self) -> list[SecretSchema]:
        secrets = self.secret_repository.get_secrets()
        return secrets

    def get_secret_by_access_key(self, access_key: str) -> str:
        if secret := self.secret_cache_repository.get_secret_by_access_key(access_key=access_key):
            encrypted_secret = decrypt(secret)
            print('\n from redis \n')
            return encrypted_secret
        if secret := self.secret_repository.get_secret_by_access_key(access_key=access_key):
            encrypted_secret = decrypt(secret)
            print('\n from postgres \n')
            return encrypted_secret
        else:
            raise HTTPException(status_code=404)
    
    def create_secret_and_return_access_key(self, body: SecretCreateSchema) -> str:
        body.secret = encrypt(body.secret)
        access_key = str(uuid4())

        returned_schema = self.secret_repository.create_secret(body=body, access_key=access_key)
        self.secret_cache_repository.set_secret(access_key=access_key, secret=body)
        returned_access_key = returned_schema.access_key

        try:
            schedule_secret_deletion(access_key=access_key, ttl_seconds=body.ttl_seconds)
        except Exception as e:
            print(f"Secret created but scheduling failed: {e}")
            # Можно добавить запись в очередь для повторной попытки
        
        return access_key
    
    def delete_secret(self, access_key: str) -> None:
        try:
            self.secret_repository.delete_secret(access_key=access_key)
            self.secret_cache_repository.delete_secret_by_access_key(access_key=access_key)
            # Отменяем запланированное удаление от APScheduler
            job_id = f"delete_secret_{access_key}"
            if scheduler.get_job(job_id):
                scheduler.remove_job(job_id)
        except:
            raise HTTPException(status_code=404)