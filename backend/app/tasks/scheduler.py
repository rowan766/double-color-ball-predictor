import asyncio
from contextlib import suppress
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.db.session import SessionLocal
from app.tasks.fetch_latest_draw import fetch_latest_draw

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


def seconds_until_next_run() -> float:
    now = datetime.now(SHANGHAI_TZ)
    next_run = now.replace(hour=23, minute=59, second=0, microsecond=0)
    if next_run <= now:
        next_run = next_run + timedelta(days=1)
    return max((next_run - now).total_seconds(), 1)


async def auto_draw_sync_loop() -> None:
    while True:
        await asyncio.sleep(seconds_until_next_run())
        db = SessionLocal()
        try:
            fetch_latest_draw(db)
        finally:
            db.close()


def start_auto_draw_sync() -> asyncio.Task:
    return asyncio.create_task(auto_draw_sync_loop())


async def stop_auto_draw_sync(task: asyncio.Task | None) -> None:
    if task is None:
        return
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
