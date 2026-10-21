import csv
import html
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv

from cloud_signal.mvc.core.KitBroadcastModel import KitBroadcastModel

logger = logging.getLogger(__name__)
DEFAULT_EQUITY_MARKETS = {
    "DowJones30",
    "FTSE100",
    "FTSE250",
    "HSI",
    "MajorETFs",
    "Nasdaq100",
    "Russell1000",
    "SPDR_ETFS",
    "SPX500",
}


class EmailDigestController:
    def __init__(
        self,
        model: KitBroadcastModel,
        output_directory: Path,
        markets: Optional[set] = None,
        send_delay_minutes: int = 10,
    ) -> None:
        self.model = model
        self.output_directory = Path(output_directory)
        self.markets = (
            markets if markets is not None else DEFAULT_EQUITY_MARKETS
        )
        self.send_delay_minutes = send_delay_minutes

    @property
    def kit_configured(self) -> bool:
        return self.model.configured

    @staticmethod
    def _read_csv(path: Path) -> List[Dict[str, str]]:
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
                return list(csv.DictReader(csv_file))
        except (OSError, csv.Error):
            logger.exception("Could not read cloud aggregate %s", path)
            return []

    @staticmethod
    def _integer(value: str) -> Optional[int]:
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None

    def find_matches(self) -> List[Dict[str, str]]:
        matches: List[Dict[str, str]] = []
        for daily_path in sorted(self.output_directory.glob("*-cloud-D.csv")):
            market = daily_path.name[: -len("-cloud-D.csv")]
            if self.markets and market not in self.markets:
                continue
            weekly_path = daily_path.with_name(f"{market}-cloud-W.csv")
            if not weekly_path.is_file():
                continue

            weekly_rows = {
                row.get("Symbol", "").strip(): row
                for row in self._read_csv(weekly_path)
                if row.get("Symbol", "").strip()
                and (self._integer(row.get("1W Cloud Count", "")) or 0) > 0
            }
            for daily in self._read_csv(daily_path):
                symbol = daily.get("Symbol", "").strip()
                daily_count = self._integer(daily.get("1D Cloud Count", ""))
                weekly = weekly_rows.get(symbol)
                if not symbol or daily_count != 1 or weekly is None:
                    continue
                matches.append(
                    {
                        "date": daily.get("Date", ""),
                        "market": market,
                        "symbol": symbol,
                        "name": daily.get("Name", ""),
                        "close": daily.get("Close", ""),
                        "daily_direction": daily.get("1D Cloud Direction", ""),
                        "daily_count": str(daily_count),
                        "weekly_direction": weekly.get(
                            "1W Cloud Direction", ""
                        ),
                        "weekly_count": weekly.get("1W Cloud Count", ""),
                    }
                )
        return sorted(matches, key=lambda row: (row["market"], row["symbol"]))

    @staticmethod
    def _format_digest_html(matches: List[Dict[str, str]]) -> str:
        rows = []
        for row in matches:
            values = (
                row["market"],
                row["symbol"],
                row["name"],
                row["close"],
                f"{row['daily_direction']}/{row['daily_count']}",
                f"{row['weekly_direction']}/{row['weekly_count']}",
            )
            cells = "".join(
                f"<td>{html.escape(value)}</td>" for value in values
            )
            rows.append(f"<tr>{cells}</tr>")

        return (
            "<h2>Stocks matching 1D Cloud Count = 1 and "
            "1W Cloud Count &gt; 0</h2>"
            "<table><thead><tr><th>Market</th><th>Symbol</th><th>Name</th>"
            "<th>Close</th><th>1D direction/count</th>"
            "<th>1W direction/count</th></tr></thead><tbody>"
            + "".join(rows)
            + "</tbody></table>"
            '<p><a href="{{ unsubscribe_url }}">Unsubscribe</a></p>'
        )

    def send_digest(self) -> Dict[str, int]:
        if not self.kit_configured:
            logger.info(
                "Kit digest skipped: API key or digest tag ID is unset"
            )
            return {"matches": 0, "scheduled": 0, "skipped": 0}

        matches = self.find_matches()
        if not matches:
            logger.info("Email digest skipped: no matching stocks")
            return {"matches": 0, "scheduled": 0, "skipped": 0}

        digest_date = max(
            (row["date"] for row in matches if row["date"]),
            default=datetime.now(timezone.utc).date().isoformat(),
        )
        if self.model.broadcast_for_date(digest_date) is not None:
            logger.info("Kit digest already scheduled for %s", digest_date)
            return {"matches": len(matches), "scheduled": 0, "skipped": 1}

        now = datetime.now(timezone.utc)
        scheduled_at = now + timedelta(minutes=self.send_delay_minutes)
        payload = {
            "subject": f"Cloud Signal stock digest - {digest_date}",
            "preview_text": (
                "Stocks matching 1D Cloud Count = 1 and 1W Cloud Count > 0"
            ),
            "description": f"Cloud Signal stock digest for {digest_date}",
            "content": self._format_digest_html(matches),
            "public": False,
            "published_at": now.isoformat(),
            "send_at": scheduled_at.isoformat(),
            "subscriber_filter": [
                {
                    "all": [{"type": "tag", "ids": [self.model.tag_id]}],
                    "any": None,
                    "none": None,
                }
            ],
        }
        broadcast_id = self.model.create_broadcast(payload)
        self.model.record_broadcast(
            digest_date, broadcast_id, scheduled_at.isoformat()
        )
        logger.info(
            "Kit broadcast %s scheduled for %s", broadcast_id, scheduled_at
        )
        return {"matches": len(matches), "scheduled": 1, "skipped": 0}


def create_email_digest_controller() -> EmailDigestController:
    project_root = Path(__file__).resolve().parents[3]
    load_dotenv(project_root / ".env", override=False)
    configured_database = os.environ.get("DIGEST_STATE_DB")
    database_path = (
        Path(configured_database)
        if configured_database
        else project_root / "instance" / "kit_digest_deliveries.sqlite3"
    )
    configured_markets = os.environ.get("EMAIL_DIGEST_MARKETS")
    markets = (
        {
            name.strip()
            for name in configured_markets.split(",")
            if name.strip()
        }
        if configured_markets is not None
        else DEFAULT_EQUITY_MARKETS
    )
    model = KitBroadcastModel(
        database_path=database_path,
        api_key=os.environ.get("KIT_API_KEY", ""),
        tag_id=int(os.environ.get("KIT_DIGEST_TAG_ID", "0")),
        api_base_url=os.environ.get(
            "KIT_API_BASE_URL", "https://api.kit.com/v4"
        ),
    )
    return EmailDigestController(
        model=model,
        output_directory=Path(
            os.environ.get(
                "CLOUD_OUTPUT_DIRECTORY", project_root / "output" / "cloud"
            )
        ),
        markets=markets,
        send_delay_minutes=int(os.environ.get("KIT_SEND_DELAY_MINUTES", "10")),
    )
