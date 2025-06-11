from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.models import RequestLog

async def log_request(request: Request, call_next, db: AsyncSession):
    response = await call_next(request)

    if request.url.path.startswith(("/docs", "/openapi.json", "/redoc")):
        return response
    
    log = RequestLog(
        ip=request.client.host if request.client else "unknown",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code
    )
    
    db.add(log)
    await db.commit()
    
    return response
