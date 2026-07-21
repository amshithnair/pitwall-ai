# Replay Engine Architecture

The Replay Engine is a core architectural pillar of PitWall AI. The platform does not treat historical data differently from live data. To ensure that prediction models and AI orchestrators behave identically during development and production, all historical races must be "played back" as a stream of Canonical Events.

## 1. Replay Philosophy

- **Absolute Parity**: The Replay Engine publishes the exact same Protocol Buffer payloads to the exact same Redis Stream topics as the live Normalizer.
- **Determinism**: Replaying a session with the same parameters must yield the exact same sequence of events.
- **Isolation**: Replay events must not contaminate the live database or interfere with active sessions.

## 2. Replay Identifiers

To prevent data contamination, when a session is replayed, the Replay Engine generates a new UUID for the replay instance.
- **Original Session ID**: `2024-silverstone-race`
- **Replay Session ID**: `replay-5a3d-4c2b-2024-silverstone-race`

The Replay Engine rewrites the `session_id` in the Event Envelope before publishing. Downstream services use this ID to isolate state.

## 3. Supported Capabilities

- **Playback Speeds**: 1x (Real-time), 5x, 10x, 20x (Batch processing).
- **Pause/Resume**: The engine can halt the publishing loop.
- **Seek**: Jump forward or backward. (Implementation requires resetting downstream service state and fast-forwarding the event log up to the seek point).
- **Jump to Lap**: Seek to the timestamp of the `lap.started` event for the specified lap.
- **Restart**: Reset the replay session state and begin from sequence 0.

## 4. Synchronization Guarantees

Event timestamps in a race are critical. The Replay Engine maintains an internal clock that ticks at the specified speed multiplier.

1. The Engine queries TimescaleDB for the next block of events ordered by original `timestamp`.
2. It calculates the delta between the current event and the next event.
3. It sleeps for `(delta / speed_multiplier)` before publishing the next event.
4. The published event retains its *original* historical timestamp in the envelope, allowing downstream prediction models to function correctly, while the time *between* event arrivals is compressed.

## 5. Event Scheduling & Storage

- **Source of Truth**: `TimescaleDB` holds the immutable log of all historical events.
- **Buffering**: The Replay Engine reads events from TimescaleDB in chunks (e.g., 5-minute windows) to prevent memory exhaustion and reduce database load.

## 6. Architecture Diagram

```text
TimescaleDB (Historical Events)
      │
      ▼ (Chunked SQL SELECTs ordered by timestamp)
Replay Engine (State Machine: Playing, Paused)
      │
      ▼ (Sleeps according to speed_multiplier)
      │ (Rewrites session_id to replay_id)
      ▼
Redis Streams (Topic: events.canonical)
      │
      ▼
Downstream Services (Analytics, AI, Dashboard)
```
