from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.database.deps import get_db
from app.lib.client import APIClient

scheduler = AsyncIOScheduler()


async def update_data_mutual_fund_data():
    db = next(get_db())
    client = APIClient()
    try:
        await client.ingest_all_data(db)
    finally:
        db.close()


def schedule_jobs():
    scheduler.add_job(
        update_data_mutual_fund_data,
        IntervalTrigger(hours=1),
        id="update_complete_mutual_fund_data",
        name="Update mutual fund data hourly",
        replace_existing=True,
    )
