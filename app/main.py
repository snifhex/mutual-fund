from fastapi import APIRouter, FastAPI

from app.api.router import api_router
from app.core.database.db import Base, engine

app = FastAPI(
    title="Mutual Fund API",
    description="Simple mutual fund api built with fastapi.",
    version="1.0.0",
    docs_url="/docs",
)

Base.metadata.create_all(bind=engine)


api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(api_router)
app.include_router(api_v1_router)
