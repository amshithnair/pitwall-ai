import threading


class PlaybackController:
    """Provides thread-safe state control for replay sessions."""

    def __init__(self):
        self._state_lock = threading.Lock()
        self._state = "STOPPED"
        self._speed = 1.0
        self._pause_event = threading.Event()
        self._pause_event.set()  # Set means "not paused" (can proceed)

    @property
    def state(self) -> str:
        with self._state_lock:
            return self._state

    @property
    def speed(self) -> float:
        with self._state_lock:
            return self._speed

    def start(self) -> None:
        with self._state_lock:
            self._state = "PLAYING"
            self._pause_event.set()

    def stop(self) -> None:
        with self._state_lock:
            self._state = "STOPPED"
            self._pause_event.set()  # Unblock any sleeping threads so they can exit

    def pause(self) -> None:
        with self._state_lock:
            if self._state == "PLAYING":
                self._state = "PAUSED"
                self._pause_event.clear()

    def resume(self) -> None:
        with self._state_lock:
            if self._state == "PAUSED":
                self._state = "PLAYING"
                self._pause_event.set()

    def set_speed(self, speed: float) -> None:
        if speed <= 0:
            raise ValueError("Speed must be positive")
        with self._state_lock:
            self._speed = speed

    def wait_if_paused(self) -> None:
        """Blocks if paused. Returns immediately if playing."""
        self._pause_event.wait()
