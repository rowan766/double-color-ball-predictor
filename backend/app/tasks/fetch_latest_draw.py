from datetime import date, timedelta
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from sqlalchemy.orm import Session

from app.schemas.draw import LotteryDrawCreate, LotteryDrawImportResult
from app.services.draw_service import DrawService


def fetch_latest_draw(db: Session, days: int = 30) -> LotteryDrawImportResult:
    """Fetch recent SSQ draw data and import it idempotently."""
    day_end = date.today()
    day_start = day_end - timedelta(days=days)
    params = urlencode(
        {
            "name": "ssq",
            "issueCount": "",
            "issueStart": "",
            "issueEnd": "",
            "dayStart": day_start.isoformat(),
            "dayEnd": day_end.isoformat(),
            "pageNo": "1",
            "pageSize": "100",
            "week": "",
            "systemType": "PC",
        }
    )
    request = Request(
        f"https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?{params}",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.cwl.gov.cn/",
        },
    )
    with urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))

    rows = payload.get("result") or []
    draws = [
        LotteryDrawCreate(
            issue_no=str(row["code"]),
            draw_date=str(row["date"])[:10],
            red_numbers=[int(number) for number in str(row["red"]).split(",")],
            blue_number=int(row["blue"]),
            source="cwl.gov.cn",
        )
        for row in rows
    ]
    if not draws:
        return LotteryDrawImportResult(
            imported_count=0,
            created_count=0,
            updated_count=0,
            skipped_count=0,
            latest_issue_no=None,
        )
    return DrawService(db).import_draws(draws=draws, overwrite=True)
