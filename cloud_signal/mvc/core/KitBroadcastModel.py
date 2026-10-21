import json
import sqlite3
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen


class KitBroadcastModel:
    def __init__(
        self,
        database_path: Path,
        api_key: str,
        tag_id: int,
        api_base_url: str = "https://api.kit.com/v4",
    ) -> None:
        self.database_path = Path(database_path)
        self.api_key = api_key
        self.tag_id = tag_id
        self.api_base_url = api_base_url.rstrip("/")
        self._initialize_database()

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.tag_id > 0)

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self.database_path, timeout=15)

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS digest_broadcasts (
                    digest_date TEXT PRIMARY KEY,
                    broadcast_id INTEGER NOT NULL,
                    scheduled_at TEXT NOT NULL
                )
                """
            )

    def broadcast_for_date(self, digest_date: str) -> Optional[int]:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT broadcast_id FROM digest_broadcasts WHERE digest_date = ?",
                (digest_date,),
            ).fetchone()
        return row[0] if row else None

    def create_broadcast(self, payload: dict) -> int:
        request = Request(
            f"{self.api_base_url}/broadcasts",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-Kit-Api-Key": self.api_key,
            },
            method="POST",
        )
        with urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        broadcast_id = result.get("broadcast", {}).get("id")
        if not isinstance(broadcast_id, int):
            raise RuntimeError("Kit API response did not include a broadcast ID")
        return broadcast_id

    def record_broadcast(
        self, digest_date: str, broadcast_id: int, scheduled_at: str
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO digest_broadcasts
                    (digest_date, broadcast_id, scheduled_at)
                VALUES (?, ?, ?)
                """,
                (digest_date, broadcast_id, scheduled_at),
            )