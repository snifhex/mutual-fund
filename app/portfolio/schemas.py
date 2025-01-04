from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateOrderRequest(BaseModel):
    scheme_id: str
    amount: float = Field(..., gt=0)
    folio_number: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "scheme_id": "1",
                "amount": 1000,
                "folio_number": "1234567890",
            }
        }
    )


class OrderResponse(BaseModel):
    scheme_id: str
    amount: float
    units: Optional[float] = None
    nav: Optional[float] = None
    status: str
    message: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "scheme_id": "1",
                "amount": 1000,
                "status": "completed",
                "message": "Order placed successfully",
            }
        }
    )


class InvestmentDetail(BaseModel):
    fund_house: str
    scheme_code: str
    scheme_name: str
    scheme_type: str
    scheme_category: str
    purchase_nav: float
    units: float
    purchase_date: datetime
    purchase_price: float
    current_value: float
    current_nav: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fund_house": "Axis Mutual Fund",
                "scheme_code": "123456",
                "scheme_name": "Axis Bluechip Fund",
                "scheme_type": "Open Ended Schemes",
                "scheme_category": "Equity",
                "purchase_nav": 100.0,
                "units": 100.0,
                "purchase_date": "2021-01-01",
                "purchase_price": 100.0,
                "current_value": 100.0,
                "current_nav": 100.0,
            }
        }
    )


class PortfolioResponse(BaseModel):
    invested_amount: float
    current_value: float
    total_pnl: float
    investments: List[InvestmentDetail]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "invested_amount": 1000,
                "current_value": 1000,
                "total_pnl": 0,
                "investments": [],
            }
        }
    )
