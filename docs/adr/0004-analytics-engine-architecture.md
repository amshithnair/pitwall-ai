# 4. Analytics Engine Architecture

Date: 2024-10-26

## Status
Accepted

## Context
The PitWall AI platform requires an independent subsystem to perform deterministic analysis of telemetry data (e.g., speed, gears, lap times) without introducing unpredictable LLM outputs. This data is essential for both real-time dashboards and future Strategy/Prediction engines.

## Decision
1. **Stateful Telemetry Engine:** A dedicated `telemetry-engine` service will consume raw Canonical Events, process them, and output Analytics Events. 
2. **Explicit Protobuf Schemas:** Instead of dynamic JSON, we updated `categories.proto` with strictly-typed `LapAnalytics`, `DriverAnalytics`, and `SectorAnalytics`.
3. **TimescaleDB for High-Frequency Data:** We are using raw `asyncpg` combined with TimescaleDB hypertables to optimize the storage and query speed of massive arrays of telemetry data. This is necessary to support 20x replay speeds. ORMs like SQLAlchemy are reserved for business/metadata layers to avoid insertion bottlenecks in the telemetry loop.

## Consequences
- **Pros:** Fast, typed, structured, and completely separated from experimental AI modules. High replay performance.
- **Cons:** Maintaining state across the processors requires careful memory management, especially for historical replays spanning long races.
