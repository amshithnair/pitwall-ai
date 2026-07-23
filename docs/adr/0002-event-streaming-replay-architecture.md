# 2. Event Streaming and Replay Architecture

Date: 2024-10-25

## Status
Accepted

## Context
PitWall AI needs to stream live race data, replay historical races with exact timing, and run AI prediction models. We require an event broker that guarantees chronological delivery, and a Replay Engine that handles time synchronization deterministically without contaminating the database.

## Decision
1. **Abstract Event Broker:** We implement an abstract `EventPublisher` and `EventSubscriber` interface in `libs/events`. This prevents hard-coupling to a specific message queue.
2. **Redis Streams as Transport:** The initial implementation uses Redis Streams. It provides Consumer Groups for scaling and pending message tracking.
3. **Replay Engine Service:** A standalone `replay-engine` service fetches chunks of data from TimescaleDB and publishes them to Redis.
4. **Replay Clock:** A custom `ReplayClock` scales virtual time using a `speed_multiplier` but maintains original message timestamps so downstream AI models receive data consistently.
5. **Validation and Monitoring:** Events are validated for schema integrity before publishing. Prometheus metrics (latency, backlogs, throughput) are emitted.

## Consequences
- **Pros:** We decouple the transport mechanism from application logic. Replay guarantees exact parity between live and historical data flows.
- **Cons:** Additional complexity in maintaining virtual time in the Replay Engine. Downstream consumers must correctly use the event timestamp rather than wall-clock time.
