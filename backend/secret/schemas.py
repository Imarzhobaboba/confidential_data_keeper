from pydantic import BaseModel
from datetime import datetime

class SecretCreateSchema(BaseModel):
    secret: str
    ttl_seconds: int

class SecretSchema(BaseModel):
    access_key: str
    secret: str
    expires_at: datetime

    class Config:
        from_attributes = True