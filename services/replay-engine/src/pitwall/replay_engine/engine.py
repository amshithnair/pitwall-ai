import logging
import threading
import uuid

from pitwall.events.broker import EventPublisher
from pitwall.events.replay import PlaybackController, ReplayClock
from pitwall.replay_engine.store import EventStore

logger = logging.getLogger(__name__)


class ReplayEngine:
    def __init__(self, publisher: EventPublisher, store: EventStore):
        self.publisher = publisher
        self.store = store
        self.clock = ReplayClock()
        self.controller = PlaybackController()
        self.worker_thread: threading.Thread | None = None
        self.current_session_id: str | None = None
        self.replay_id: str | None = None

    def start(self, session_id: str, speed: float = 1.0) -> str:
        if self.controller.state != "STOPPED":
            raise ValueError("Replay already running")

        self.current_session_id = session_id
        self.replay_id = f"replay-{uuid.uuid4().hex[:8]}-{session_id}"

        self.controller.set_speed(speed)
        self.clock.set_speed(speed)
        self.clock.start()
        self.controller.start()

        self.worker_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.worker_thread.start()
        return self.replay_id

    def pause(self) -> None:
        self.controller.pause()
        self.clock.pause()

    def resume(self) -> None:
        self.controller.resume()
        self.clock.resume()

    def stop(self) -> None:
        self.controller.stop()
        if self.worker_thread:
            self.worker_thread.join(timeout=2.0)

    def set_speed(self, speed: float) -> None:
        self.controller.set_speed(speed)
        self.clock.set_speed(speed)

    def _run_loop(self) -> None:
        logger.info(f"Starting replay loop for session {self.current_session_id}")
        try:
            iterator = self.store.get_event_iterator(self.current_session_id)
            first_event = next(iterator, None)
            if not first_event:
                logger.info("No events found for session")
                self.stop()
                return

            last_event_time = first_event.timestamp.timestamp()
            self.publisher.publish(first_event, is_live=False, replay_id=self.replay_id)

            for event in iterator:
                if self.controller.state == "STOPPED":
                    break

                self.controller.wait_if_paused()

                current_event_time = event.timestamp.timestamp()
                delta = current_event_time - last_event_time

                if delta > 0:
                    self.clock.sleep_virtual(delta)

                self.publisher.publish(event, is_live=False, replay_id=self.replay_id)
                last_event_time = current_event_time

        except Exception as e:
            logger.error(f"Error in replay loop: {e}")
        finally:
            self.controller.stop()
            logger.info("Replay loop finished")
