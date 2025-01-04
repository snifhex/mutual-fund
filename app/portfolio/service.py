from datetime import datetime

from app.core.database.deps import db_dependency
from app.funds.models import MutualFundScheme
from app.portfolio.models import Investment, Portfolio
from app.portfolio.schemas import CreateOrderRequest, InvestmentDetail, OrderResponse, PortfolioResponse


async def create_buy_order(db: db_dependency, user_id: int, order_data: CreateOrderRequest) -> OrderResponse:
    scheme = db.query(MutualFundScheme).filter(MutualFundScheme.id == order_data.scheme_id).first()

    if not scheme:
        return OrderResponse(
            scheme_id=order_data.scheme_id, amount=order_data.amount, status="failed", message="Invalid scheme ID"
        )

    if float(order_data.amount) < float(scheme.last_nav):
        return OrderResponse(
            scheme_id=order_data.scheme_id,
            amount=order_data.amount,
            status="failed",
            message=f"Minimum investment amount is {scheme.last_nav}",
        )

    try:
        units = order_data.amount / scheme.last_nav

        portfolio = get_or_create_portfolio(db, user_id)
        investment = Investment(
            portfolio_id=portfolio.id,
            scheme_id=scheme.id,
            units=units,
            purchase_price=order_data.amount,
            current_price=scheme.last_nav,
            purchase_date=datetime.now(),
        )

        db.add(investment)
        db.commit()

        return OrderResponse(
            scheme_id=scheme.id,
            amount=order_data.amount,
            units=units,
            nav=scheme.last_nav,
            status="completed",
            message="Order placed successfully",
        )

    except Exception as e:
        return OrderResponse(
            scheme_id=order_data.scheme_id,
            amount=order_data.amount,
            status="failed",
            message=str(e),
        )


def get_or_create_portfolio(db: db_dependency, user_id: int) -> Portfolio:
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user_id).first()
    if not portfolio:
        portfolio = Portfolio(user_id=user_id)
        db.add(portfolio)
        db.commit()
    return portfolio


async def get_portfolio(db: db_dependency, user_id: int) -> PortfolioResponse:
    portfolio = get_or_create_portfolio(db, user_id)

    total_invested = 0
    total_current = 0
    investments = []

    for inv in portfolio.investments:
        scheme = db.query(MutualFundScheme).filter(MutualFundScheme.id == inv.scheme_id).first()

        if not scheme:
            continue

        current_value = inv.units * scheme.last_nav
        total_invested += inv.purchase_price
        total_current += current_value

        investments.append(
            InvestmentDetail(
                fund_house=scheme.fund_family.name,
                scheme_code=scheme.id,
                scheme_name=scheme.scheme_name,
                scheme_type=scheme.scheme_type,  
                scheme_category=scheme.scheme_category,
                purchase_nav=inv.purchase_price / inv.units,
                units=inv.units,
                purchase_date=inv.purchase_date,
                purchase_price=inv.purchase_price,
                current_value=current_value,
                current_nav=scheme.last_nav,
            )
        )

    return PortfolioResponse(
        invested_amount=total_invested,
        current_value=total_current,
        total_pnl=total_current - total_invested,
        investments=investments,
    )
