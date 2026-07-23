# 5. Redis Stream Topology and Delivery Guarantees

Date: 2026-07-21

## Status

Accepted

## Context

PitWall AI uses a Canonical Event Architecture where all system components communicate exclusively via standardized events. Given the high-frequency nature of Formula 1 telemetry and race events, we need a lightweight, low-latency, and durable message broker to route these events from the Provider Adapters to various consumers (Analytics, Database Storage, AI Orchestrator, Strategy Engine, Dashboard).

We previously chose Protocol Buffers for event serialization (ADR-0002) and TimescaleDB for telemetry storage (ADR-0003). We now need to define the exact topology for routing these events through Redis Streams, which serves as our central nervous system.

Specifically, we need to handle both **live race streams** and **historical replays** without modifying consumer logic, ensuring consumers treat live and replay events identically.

## Decision

We will use **Redis Streams** as the primary message broker with the following topology and delivery guarantees:

### Stream Topics

- `pitwall:live:events`: The primary stream for all real-time events ingested during a live session.
- `pitwall:replay:{replay_id}:events`: Dedicated streams for individual replay sessions. The Replay Engine will spin up a new stream for each active replay, allowing multiple isolated replays to run concurrently.

Consumers that are context-aware (e.g., the Dashboard client connected to a specific replay session) will subscribe to the specific `pitwall:replay:{replay_id}:events` stream. Global consumers that record data (e.g., TimescaleDB Storage Sink) will only subscribe to `pitwall:live:events` to avoid duplicating historical data.

### Consumer Groups

Consumers will use Redis Consumer Groups to ensure load balancing and state tracking:
- **Storage Sink Group**: (`group:storage_sink`) Consumes from `pitwall:live:events` to persist data into TimescaleDB and PostgreSQL.
- **Analytics Engine Group**: (`group:analytics`) Consumes from live and replay streams to run real-time strategy models.
- **AI Orchestrator Group**: (`group:ai_orchestrator`) Consumes from live and replay streams for generative insights.

### Delivery Guarantees

We adopt an **At-Least-Once** delivery guarantee model.
- Producers `XADD` to the stream.
- Consumers `XREADGROUP`, process the message, and then issue an `XACK`.
- If a consumer crashes before `XACK`, the message remains in the Pending Entries List (PEL). A background worker (or the consumer itself on startup) will run `XPENDING` and `XCLAIM` to reprocess unacknowledged messages.

### Idempotency Requirements

Because of the At-Least-Once delivery guarantee, all downstream consumers (especially the Storage Sink writing to TimescaleDB) **must be idempotent**.
- TimescaleDB inserts will use `ON CONFLICT DO NOTHING` based on the event's unique primary keys (e.g., `(session_id, driver_id, timestamp)` for telemetry, or `event_id` for distinct events).
- AI components will utilize caching or state tracking to prevent duplicate insight generation for the same `event_id`.

## Consequences

- **Positive:** Redis Streams provide very low latency and native Pub/Sub features with durability (via Consumer Groups and PEL).
- **Positive:** Creating unique streams for each replay session ensures perfect isolation and allows multi-tenant replays.
- **Negative:** Downstream systems bear the burden of idempotency.
- **Negative:** Redis memory must be carefully managed. We will configure `MAXLEN` on streams (e.g., `XADD ... MAXLEN ~ 1000000`) to prevent memory exhaustion, as older events are durably stored in TimescaleDB.
