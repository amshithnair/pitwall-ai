import time

from pitwall.events.replay.clock import ReplayClock


def test_clock_normal_speed():
    clock = ReplayClock(speed_multiplier=1.0)
    clock.start()
    time.sleep(0.1)
    clock.pause()
    elapsed = clock.get_elapsed_virtual_time()
    assert 0.05 <= elapsed <= 0.15


def test_clock_fast_speed():
    clock = ReplayClock(speed_multiplier=10.0)
    clock.start()
    time.sleep(0.1)
    clock.pause()
    elapsed = clock.get_elapsed_virtual_time()
    assert 0.5 <= elapsed <= 1.5


def test_clock_pause_resume():
    clock = ReplayClock(speed_multiplier=1.0)
    clock.start()
    time.sleep(0.1)
    clock.pause()
    elapsed_paused1 = clock.get_elapsed_virtual_time()
    time.sleep(0.1)
    elapsed_paused2 = clock.get_elapsed_virtual_time()
    assert elapsed_paused1 == elapsed_paused2

    clock.resume()
    time.sleep(0.1)
    clock.pause()
    elapsed_final = clock.get_elapsed_virtual_time()
    assert elapsed_final > elapsed_paused1
