from typing import List

from fastapi import HTTPException

from app.core.database.deps import db_dependency
from app.funds import models, schemas


def get_all_mutual_fund_families(db: db_dependency) -> List[schemas.MutualFundFamilyResponse]:
    fund_families = db.query(models.MutualFundFamily).all()
    return [
        schemas.MutualFundFamilyResponse(id=str(family.id), name=family.name, is_active=family.is_active)
        for family in fund_families
    ]


def get_all_schemes(db: db_dependency, fund_family_id: str, scheme_type: str) -> List[schemas.MutualFundSchemeResponse]:
    fund_schemes = (
        db.query(models.MutualFundScheme)
        .filter(
            models.MutualFundScheme.fund_family_id == fund_family_id,
            models.MutualFundScheme.scheme_type == scheme_type,
        )
        .all()
    )
    return [
        schemas.MutualFundSchemeResponse(
            id=scheme.id,
            scheme_code=scheme.scheme_code,
            scheme_name=scheme.scheme_name,
            scheme_type=scheme.scheme_type,
            scheme_category=scheme.scheme_category,
            isin_payout=scheme.isin_payout,
            isin_reinvestment=scheme.isin_reinvestment,
            nav=scheme.last_nav,
            nav_date=scheme.last_nav_date,
            nav_last_updated=scheme.nav_last_updated,
            fund_family=scheme.fund_family.name,
        )
        for scheme in fund_schemes
    ]


def get_scheme_by_id(db: db_dependency, scheme_id: str) -> schemas.MutualFundSchemeResponse:
    fund_scheme = db.query(models.MutualFundScheme).filter(models.MutualFundScheme.id == scheme_id).first()
    if not fund_scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return schemas.MutualFundSchemeResponse(
        id=fund_scheme.id,
        scheme_code=fund_scheme.scheme_code,
        scheme_name=fund_scheme.scheme_name,
        scheme_type=fund_scheme.scheme_type,
        scheme_category=fund_scheme.scheme_category,
        isin_payout=fund_scheme.isin_payout,
        isin_reinvestment=fund_scheme.isin_reinvestment,
        fund_family=fund_scheme.fund_family.name,
        nav=fund_scheme.last_nav,
        nav_date=fund_scheme.last_nav_date,
        nav_last_updated=fund_scheme.nav_last_updated,
    )
