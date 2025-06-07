from fastapi import FastAPI

from secret.handlers import router as secret_router
from infrastructure.scheduler import start_scheduler


app = FastAPI()


@app.on_event("startup")
def startup_event():
    start_scheduler()

app.include_router(secret_router)
