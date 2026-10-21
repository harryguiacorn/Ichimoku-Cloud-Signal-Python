import csv
import json
from datetime import datetime

from cloud_signal.mvc.controllers.EmailDigestController import (
    EmailDigestController,
)
from cloud_signal.mvc.core.KitBroadcastModel import KitBroadcastModel


def _write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_find_matches_joins_daily_and_weekly_counts(tmp_path):
    daily_path = tmp_path / "SPX500-cloud-D.csv"
    weekly_path = tmp_path / "SPX500-cloud-W.csv"
    _write_csv(
        daily_path,
        [
            "Date",
            "Symbol",
            "Name",
            "Close",
            "1D Cloud Direction",
            "1D Cloud Count",
        ],
        [
            {
                "Date": "2026-09-29",
                "Symbol": "AAA",
                "Name": "A",
                "Close": "10",
                "1D Cloud Direction": "1",
                "1D Cloud Count": "1",
            },
            {
                "Date": "2026-09-29",
                "Symbol": "BBB",
                "Name": "B",
                "Close": "20",
                "1D Cloud Direction": "1",
                "1D Cloud Count": "2",
            },
            {
                "Date": "2026-09-29",
                "Symbol": "CCC",
                "Name": "C",
                "Close": "30",
                "1D Cloud Direction": "-1",
                "1D Cloud Count": "1",
            },
        ],
    )
    _write_csv(
        weekly_path,
        [
            "Date",
            "Symbol",
            "Name",
            "Close",
            "1W Cloud Direction",
            "1W Cloud Count",
        ],
        [
            {
                "Date": "2026-09-28",
                "Symbol": "AAA",
                "Name": "A",
                "Close": "9",
                "1W Cloud Direction": "1",
                "1W Cloud Count": "4",
            },
            {
                "Date": "2026-09-28",
                "Symbol": "BBB",
                "Name": "B",
                "Close": "19",
                "1W Cloud Direction": "1",
                "1W Cloud Count": "3",
            },
            {
                "Date": "2026-09-28",
                "Symbol": "CCC",
                "Name": "C",
                "Close": "29",
                "1W Cloud Direction": "-1",
                "1W Cloud Count": "0",
            },
        ],
    )
    model = KitBroadcastModel(
        tmp_path / "kit.sqlite3", api_key="test-api-key", tag_id=42
    )
    controller = EmailDigestController(model, tmp_path)

    matches = controller.find_matches()

    assert [
        (row["symbol"], row["daily_count"], row["weekly_count"])
        for row in matches
    ] == [("AAA", "1", "4")]


def test_digest_schedules_one_tagged_kit_broadcast(tmp_path, monkeypatch):
    daily_path = tmp_path / "SPX500-cloud-D.csv"
    weekly_path = tmp_path / "SPX500-cloud-W.csv"
    _write_csv(
        daily_path,
        [
            "Date",
            "Symbol",
            "Name",
            "Close",
            "1D Cloud Direction",
            "1D Cloud Count",
        ],
        [
            {
                "Date": "2026-10-08",
                "Symbol": "AAA",
                "Name": "A & B",
                "Close": "10",
                "1D Cloud Direction": "1",
                "1D Cloud Count": "1",
            }
        ],
    )
    _write_csv(
        weekly_path,
        [
            "Date",
            "Symbol",
            "Name",
            "Close",
            "1W Cloud Direction",
            "1W Cloud Count",
        ],
        [
            {
                "Date": "2026-10-05",
                "Symbol": "AAA",
                "Name": "A & B",
                "Close": "9",
                "1W Cloud Direction": "1",
                "1W Cloud Count": "4",
            }
        ],
    )

    model = KitBroadcastModel(
        tmp_path / "kit.sqlite3", api_key="test-api-key", tag_id=42
    )
    controller = EmailDigestController(model, tmp_path, send_delay_minutes=10)
    captured = {}

    class MockResponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return b'{"broadcast":{"id":123}}'

    def fake_urlopen(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return MockResponse()

    monkeypatch.setattr(
        "cloud_signal.mvc.core.KitBroadcastModel.urlopen", fake_urlopen
    )

    first_result = controller.send_digest()
    second_result = controller.send_digest()

    request = captured["request"]
    payload = json.loads(request.data.decode("utf-8"))
    scheduled_at = datetime.fromisoformat(payload["send_at"])
    now = datetime.now().astimezone()
    assert first_result == {"matches": 1, "scheduled": 1, "skipped": 0}
    assert second_result == {"matches": 1, "scheduled": 0, "skipped": 1}
    assert request.full_url == "https://api.kit.com/v4/broadcasts"
    assert request.get_header("X-kit-api-key") == "test-api-key"
    assert payload["subscriber_filter"] == [
        {"all": [{"type": "tag", "ids": [42]}], "any": None, "none": None}
    ]
    assert payload["send_at"]
    assert scheduled_at > now
    assert "A &amp; B" in payload["content"]
    assert "{{ unsubscribe_url }}" in payload["content"]
    assert model.broadcast_for_date("2026-10-08") == 123
