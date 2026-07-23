import time


class ReplayClock:
    """Manages virtual time progression for the replay engine."""

    def __init__(self, speed_multiplier: float = 1.0):
        self.speed_multiplier = speed_multiplier
        self.is_paused = False
        self._last_tick: float | None = None
        self._accumulated_virtual_time: float = 0.0

    def start(self) -> None:
        self.is_paused = False
        self._last_tick = time.monotonic()

    def pause(self) -> None:
        if not self.is_paused:
            self._update_virtual_time()
            self.is_paused = True

    def resume(self) -> None:
        if self.is_paused:
            self._last_tick = time.monotonic()
            self.is_paused = False

    def set_speed(self, speed: float) -> None:
        if speed <= 0:
            raise ValueError("Speed multiplier must be positive")
        self._update_virtual_time()
        self.speed_multiplier = speed

    def _update_virtual_time(self) -> None:
        if not self.is_paused and self._last_tick is not None:
            now = time.monotonic()
            delta_real = now - self._last_tick
            self._accumulated_virtual_time += delta_real * self.speed_multiplier
            self._last_tick = now

    def get_elapsed_virtual_time(self) -> float:
        """Returns elapsed virtual time in seconds."""
        self._update_virtual_time()
        return self._accumulated_virtual_time

    def sleep_virtual(self, virtual_seconds: float) -> None:
        """Sleeps for a duration in virtual time, scaled by speed_multiplier."""
        if virtual_seconds <= 0:
            return

        real_seconds = virtual_seconds / self.speed_multiplier
        # A more robust implementation would interrupt sleep on pause,
        # but for our chunked loop, time.sleep is sufficient.
        time.sleep(real_seconds)
