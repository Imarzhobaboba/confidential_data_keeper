from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from secret.handlers import router as secret_router
from infrastructure.scheduler import start_scheduler
from infrastructure.database import get_db
from logger import log_request


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    start_scheduler()

app.include_router(secret_router)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    db = next(get_db())
    try:
        return await log_request(request, call_next, db)
    finally:
        db.close()
