from typing import List

from fastapi import APIRouter
from starlette import status

from app.auth.deps import user_dependecy
from app.core.database.deps import db_dependency
from app.funds import schemas, service

funds_router = APIRouter()


@funds_router.get("/families/", response_model=List[schemas.MutualFundFamilyResponse], status_code=status.HTTP_200_OK)
async def list_mutual_fund_families(db: db_dependency, user: user_dependecy):
    """
    Get all mutual fund families

    Returns names of all mutual fund families with their id
    """
    return service.get_all_mutual_fund_families(db)


@funds_router.get("/{fund_family_id}/schemes/", response_model=List[schemas.MutualFundSchemeResponse], status_code=status.HTTP_200_OK)
async def list_mutual_fund_schemes(
    db: db_dependency, user: user_dependecy, fund_family_id: str, scheme_type: str = "Open Ended Schemes"):
    """
    Get all mutual fund schemes for a given fund family

    Returns all schemes for a given fund family, Containing
    - scheme_id
    - scheme_code
    - isin_payout
    - isin_reinvestment
    - scheme_name
    - scheme_type
    - scheme_category
    - nav
    - nav_date
    - fund_family
    """
    return service.get_all_schemes(db, fund_family_id, scheme_type)


@funds_router.get("/schemes/{scheme_id}", response_model=schemas.MutualFundSchemeResponse, status_code=status.HTTP_200_OK)
async def get_mutual_fund_scheme_by_id(db: db_dependency, user: user_dependecy, scheme_id: str):
    """
    Get mutual fund scheme by id

    Returns a mutual fund scheme by id, Containing
    - scheme_id
    - scheme_code
    - isin_payout
    - isin_reinvestment
    - scheme_name
    - scheme_type
    - scheme_category
    - nav
    - nav_date
    - fund_family
    """
    return service.get_scheme_by_id(db, scheme_id)
