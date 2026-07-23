from unittest.mock import MagicMock, patch

from pitwall.provider_adapter.providers.fastf1_provider import FastF1Provider


@patch("fastf1.get_session")
@patch("fastf1.Cache.enable_cache")
def test_get_session_info(mock_enable_cache, mock_get_session, tmp_path):
    mock_session = MagicMock()
    mock_session.event.EventName = "British Grand Prix"
    mock_session.event.Country = "UK"
    mock_session.name = "Race"
    mock_session.date.isoformat.return_value = "2024-07-07T14:00:00"

    mock_get_session.return_value = mock_session

    provider = FastF1Provider(cache_dir=str(tmp_path / "cache"))
    info = provider.get_session_info(2024, "silverstone", "race")

    assert info["provider"] == "fastf1"
    assert info["country"] == "UK"
    assert info["event_name"] == "British Grand Prix"


def test_health_check(tmp_path):
    provider = FastF1Provider(cache_dir=str(tmp_path / "cache"))
    assert provider.health_check() is True
