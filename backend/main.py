from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from secret.handlers import router as secret_router
from infrastructure.scheduler import start_scheduler
from infrastructure.database import async_session
from infrastructure.models import create_tables
from logger import log_request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await create_tables()
    start_scheduler()

app.include_router(secret_router)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    async with async_session() as db:
        try:
            response = await log_request(request, call_next, db)
            return response
        except Exception as e:
            await db.rollback()
            raise
        finally:
            await db.close()
