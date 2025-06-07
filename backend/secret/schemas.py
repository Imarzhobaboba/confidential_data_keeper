from pydantic import BaseModel, Field
from datetime import datetime

class SecretCreateSchema(BaseModel):
    secret: str
    ttl_seconds: int = Field(gt=0, description="Должно быть числом больше 0")

class SecretSchema(BaseModel):
    access_key: str
    secret: str
    expires_at: datetime

    class Config:
        from_attributes = True