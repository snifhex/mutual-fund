from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MutualFundFamilyBase(BaseModel):
    name: str
    is_active: bool


class MutualFundFamilyResponse(MutualFundFamilyBase):
    id: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "1",
                "name": "Axis Mutual Fund",
                "is_active": True,
            }
        }
    )


class MutualFundSchemeBase(BaseModel):
    scheme_code: str
    isin_payout: str | None = None
    isin_reinvestment: str | None = None
    scheme_name: str
    scheme_type: str
    scheme_category: str
    nav: float | None = None
    nav_date: datetime | None = None
    nav_last_updated: datetime | None = None


class MutualFundSchemeResponse(MutualFundSchemeBase):
    id: str
    fund_family: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "1",
                "scheme_code": "123456",
                "isin_payout": "IN1234567890",
                "isin_reinvestment": "IN1234567890",
                "scheme_name": "Axis Bluechip Fund",
                "scheme_type": "Open Ended Schemes",
                "scheme_category": "Equity",
                "nav": 100.0,
                "nav_date": "2021-01-01",
                "fund_family": "Axis Mutual Fund",
            }
        }
    )
