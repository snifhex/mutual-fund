from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from app.api.router import api_router
from app.auth.router import auth_router
from app.core.database.db import Base, SessionLocal, engine
from app.core.scheduler import schedule_jobs, scheduler
from app.lib.client import APIClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    client = APIClient()
    await client.ingest_all_data(db)
    schedule_jobs()
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(
    title="Mutual Fund API",
    description="Simple mutual fund api built with fastapi.",
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan,
)

Base.metadata.create_all(bind=engine)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(api_router)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(api_v1_router)
