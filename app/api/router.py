from fastapi import APIRouter

from app.funds.router import funds_router


api_router = APIRouter()

api_router.include_router(funds_router, prefix="/mutual-funds", tags=["Mutual Funds"])

