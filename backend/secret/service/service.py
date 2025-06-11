from fastapi import HTTPException

from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime

from secret.repository.postgres import SecretRepository
from secret.repository.cache import SecretCacheRepository
from secret.schemas import SecretCreateSchema, SecretUpdateSchema

from secret.service.crypto import encrypt, decrypt
from infrastructure.scheduler import scheduler, schedule_secret_deletion, update_schedule


@dataclass
class SecretService:
    secret_repository: SecretRepository
    secret_cache_repository: SecretCacheRepository


    def get_secret_by_access_key(self, access_key: str) -> str:
        if secret := self.secret_cache_repository.get_secret_by_access_key(access_key=access_key):
            self.secret_cache_repository.refresh_ttl(access_key=access_key)
            encrypted_secret = decrypt(secret)
            print('\n from redis \n')
            return encrypted_secret
        if secret_schema := self.secret_repository.get_secret(access_key=access_key):
            self.secret_cache_repository.set_secret(access_key=access_key, secret=secret_schema.secret)
            encrypted_secret = decrypt(secret_schema.secret)
            print('\n from postgres \n')
            return encrypted_secret
        else:
            raise HTTPException(status_code=404)
    
    def create_secret_and_return_access_key(self, body: SecretCreateSchema) -> str:
        body.secret = encrypt(body.secret)
        access_key = str(uuid4())

        if created_secret := self.secret_repository.create_secret(body=body, access_key=access_key):
            self.secret_cache_repository.set_secret(access_key=access_key, secret=body.secret)
            try:
                schedule_secret_deletion(access_key=access_key, ttl_seconds=body.ttl_seconds)
            except Exception as e:
                print(f"Secret created but scheduling failed: {e}")
                # Можно добавить запись в очередь для повторной попытки
            
            return access_key
        else:
            raise HTTPException(status_code=503)
        
    def update_secret(self, access_key: str, body: SecretUpdateSchema) -> None:
        if body.secret is not None:                    
            body.secret = encrypt(body.secret)
            if self.secret_repository.update_secret(access_key=access_key, secret=body.secret) is not None:
                self.secret_cache_repository.update_value_and_refresh(access_key=access_key, new_secret=body.secret)
            else:
                raise HTTPException(status_code=404)
        
        if body.additional_ttl_seconds is not None:
            if self.secret_repository.update_time(access_key=access_key, additional_ttl_seconds=body.additional_ttl_seconds) is not None:
                self.secret_cache_repository.refresh_ttl(access_key=access_key)
                try:
                    update_schedule(access_key=access_key, additional_ttl_seconds=body.additional_ttl_seconds)
                except Exception as e:
                    print(f"Secret updated but scheduling failed: {e}")
            else:
                raise HTTPException(status_code=404)
            
        if body.secret is None and body.additional_ttl_seconds is None:
            raise HTTPException(status_code=422)
        
    
    def delete_secret(self, access_key: str) -> None:
        if self.secret_repository.delete_secret(access_key=access_key) is not None:
            self.secret_cache_repository.delete_secret_by_access_key(access_key=access_key)
            # Отменяем запланированное удаление от APScheduler
            job_id = f"delete_secret_{access_key}"
            if scheduler.get_job(job_id):
                scheduler.remove_job(job_id)
        else:
            raise HTTPException(status_code=404)
    
    def get_secret_lifetime(self, access_key: str) -> datetime | None:
        if secret_schema := self.secret_repository.get_secret(access_key=access_key):
            return secret_schema.expires_at
        else:
            raise HTTPException(status_code=404)
