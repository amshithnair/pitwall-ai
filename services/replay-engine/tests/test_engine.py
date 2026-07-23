from unittest.mock import MagicMock

from pitwall.events.broker import EventPublisher
from pitwall.replay_engine.engine import ReplayEngine
from pitwall.replay_engine.store import EventStore


def test_replay_engine_start_stop():
    mock_publisher = MagicMock(spec=EventPublisher)
    mock_store = MagicMock(spec=EventStore)

    # Mock empty iterator
    mock_store.get_event_iterator.return_value = iter([])

    engine = ReplayEngine(publisher=mock_publisher, store=mock_store)

    replay_id = engine.start("test-session")
    assert replay_id.startswith("replay-")
    assert engine.controller.state == "PLAYING"

    engine.stop()
    assert engine.controller.state == "STOPPED"
