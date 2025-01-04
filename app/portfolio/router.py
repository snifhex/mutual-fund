from fastapi import APIRouter, HTTPException, status

from app.auth.deps import user_dependecy
from app.core.database.deps import db_dependency
from app.portfolio import schemas, service

portfolio_router = APIRouter()


@portfolio_router.post("/add-mutual-fund", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
async def buy_mutual_fund(order: schemas.CreateOrderRequest, db: db_dependency, user: user_dependecy):
    """
    Buy a mutual fund

    Returns the order status, containing
    - scheme_id
    - amount
    - status
    - message
    """
    try:
        return await service.create_buy_order(db, user.get("id"), order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@portfolio_router.get("/portfolio", response_model=schemas.PortfolioResponse, status_code=status.HTTP_200_OK)
async def get_portfolio(db: db_dependency, user: user_dependecy):
    """
    Get portfolio

    Returns the portfolio, containing
    - scheme_id
    - amount
    - status
    - message
    """
    return await service.get_portfolio(db, user.get("id"))
