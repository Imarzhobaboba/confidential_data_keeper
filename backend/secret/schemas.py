from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SecretCreateSchema(BaseModel):
    secret: str
    ttl_seconds: int = Field(gt=0, le=31536000, description="Должно быть числом больше 0")

class SecretSchema(BaseModel):
    access_key: str
    secret: str
    expires_at: datetime

    class Config:
        from_attributes = True

class SecretUpdateSchema(BaseModel):
    secret: Optional[str] = Field(default=None)
    additional_ttl_seconds: Optional[int] = Field(default=None, gt=0, le=2592000, description="Количество секунд должно быть положительным")
