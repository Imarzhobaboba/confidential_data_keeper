from fastapi import FastAPI

from secret.handlers import router as secret_router
from secret.service.scheduler import start_scheduler

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Инициализация планировщика
#     scheduler_manager.init(engine)
#     yield
#     # Остановка при завершении
#     scheduler_manager.safe_shutdown()


app = FastAPI()

@app.on_event("startup")
def startup_event():
    start_scheduler()

app.include_router(secret_router)
