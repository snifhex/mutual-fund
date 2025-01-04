import json
from datetime import datetime, timedelta
from typing import Dict, List

import redis
import requests
from fastapi import HTTPException

from app.core.config import get_settings
from app.core.database.deps import db_dependency
from app.funds import models


class APIClient:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=get_settings().REDIS_HOST,
            port=get_settings().REDIS_PORT,
            db=get_settings().REDIS_DB,
            decode_responses=True,
        )
        self.api_key = get_settings().RAPIDAPI_KEY
        self.api_host = get_settings().MF_RAPIDAPI_HOST
        self.base_url = get_settings().MF_RAPIDAPI_BASE_URL

    async def _get_api_call_count(self) -> int:
        today = datetime.now().strftime("%Y-%m-%d")
        count = self.redis_client.get(f"rapidapi:calls:{today}")
        return int(count) if count else 0

    async def _increment_api_call_count(self):
        today = datetime.now().strftime("%Y-%m-%d")
        pipe = self.redis_client.pipeline()
        pipe.incr(f"rapidapi:calls:{today}")
        pipe.expire(f"rapidapi:calls:{today}", 86400)
        pipe.execute()

    async def fetch_all_mutual_fund_data(self) -> List[str]:
        call_count = await self._get_api_call_count()

        if call_count >= 950:
            raise HTTPException(status_code=429, detail="API rate limit approaching. Try again later.")

        headers = {"X-RapidAPI-Key": self.api_key, "X-RapidAPI-Host": self.api_host}

        try:
            response = requests.get(f"{self.base_url}/latest", params={"Scheme_Type": "Open"}, headers=headers)
            response.raise_for_status()
            await self._increment_api_call_count()

            return response.json()

        except Exception:
            from pathlib import Path

            return json.load(Path("app/data/mf.json").open())

    async def ingest_all_data(self, db: db_dependency):
        mutual_funds = await self.fetch_all_mutual_fund_data()

        if not mutual_funds or len(mutual_funds) == 0:
            raise HTTPException(status_code=404, detail="No mutual funds found")

        existing_families = {family.name: family for family in db.query(models.MutualFundFamily).all()}
        existing_schemes = {scheme.scheme_code: scheme for scheme in db.query(models.MutualFundScheme).all()}

        families = []
        new_schemes = []
        updated_schemes = []
        seen_families = set()

        for mutual_fund in mutual_funds:
            family_name = mutual_fund["Mutual_Fund_Family"]
            if family_name not in seen_families and family_name not in existing_families:
                families.append(
                    models.MutualFundFamily(
                        name=family_name,
                        is_active=True,
                        last_synced=datetime.now(),
                    )
                )
                seen_families.add(family_name)

        try:
            if families:
                db.bulk_save_objects(families)
                db.flush()

            family_map = {family.name: family.id for family in db.query(models.MutualFundFamily).all()}

            for mutual_fund in mutual_funds:
                scheme_code = str(mutual_fund["Scheme_Code"])
                new_nav = float(mutual_fund["Net_Asset_Value"])
                new_nav_date = datetime.strptime(mutual_fund["Date"], "%d-%b-%Y")

                if scheme_code in existing_schemes:
                    existing_scheme = existing_schemes[scheme_code]
                    if existing_scheme.last_nav != new_nav or existing_scheme.last_nav_date != new_nav_date:
                        existing_scheme.last_nav = new_nav
                        existing_scheme.last_nav_date = new_nav_date
                        existing_scheme.nav_last_updated = datetime.now()
                        updated_schemes.append(existing_scheme)
                else:
                    new_schemes.append(
                        models.MutualFundScheme(
                            scheme_code=scheme_code,
                            isin_payout=None
                            if mutual_fund["ISIN_Div_Payout_ISIN_Growth"] in ["-", ""]
                            else mutual_fund["ISIN_Div_Payout_ISIN_Growth"],
                            isin_reinvestment=None
                            if mutual_fund["ISIN_Div_Reinvestment"] in ["-", ""]
                            else mutual_fund["ISIN_Div_Reinvestment"],
                            scheme_name=mutual_fund["Scheme_Name"],
                            scheme_type=mutual_fund["Scheme_Type"],
                            scheme_category=mutual_fund["Scheme_Category"],
                            fund_family_id=family_map[mutual_fund["Mutual_Fund_Family"]],
                            last_nav=new_nav,
                            last_nav_date=new_nav_date,
                        )
                    )

            if new_schemes:
                db.bulk_save_objects(new_schemes)
            if updated_schemes:
                db.bulk_save_objects(updated_schemes)
            db.commit()

            return {
                "new_families": len(families),
                "new_schemes": len(new_schemes),
                "updated_schemes": len(updated_schemes),
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to bulk insert data: {e!s}") from e

    async def get_nav_from_cache(self, scheme_code: str) -> Dict | None:
        data = self.redis_client.get(f"nav:{scheme_code}")
        return eval(data) if data else None

    async def set_nav_cache(self, scheme_code: str, nav_data: Dict):
        self.redis_client.setex(
            f"nav:{scheme_code}",
            timedelta(hours=1),
            str(nav_data),
        )