from datetime import datetime, timezone, timedelta
import utils


def test_is_past_iso_date():
    assert utils.is_past_iso_date("2020-01-01T12:00:00Z") == True
    assert utils.is_past_iso_date("2099-01-01T12:00:00+00:00") == False

    hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    assert utils.is_past_iso_date(hour_ago, timedelta(hours=2)) == False
    assert utils.is_past_iso_date(hour_ago, timedelta(minutes=30)) == True
