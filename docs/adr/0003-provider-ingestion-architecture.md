# 3. Provider Ingestion Architecture

Date: 2024-10-26

## Status
Accepted

## Context
Formula 1 data comes from multiple sources (FastF1, OpenF1, FIA Timing). The platform requires a unified representation of this data (Canonical Events) so downstream systems (AI, analytics, UI) don't need to know the origin of the data. Furthermore, data ingestion pipelines often deal with rate limiting, timeouts, and dirty data.

## Decision
1. **Decoupled Architecture:** We split ingestion into two distinct services:
   - `provider-adapter`: Fetches raw data from external APIs, handles retries (`tenacity`), manages local caching, and pushes raw payloads to a Redis stream.
   - `normalizer`: Consumes raw payloads from the stream, maps them into strictly typed `PitWallEvent` protobuf structures, and publishes them to the platform's primary Canonical Event stream.
2. **Abstract Provider Interface:** The `provider-adapter` uses an abstract `BaseProvider` interface so that introducing a new data source (e.g., OpenF1) does not break existing logic.
3. **Caching Strategy:**
   - `fastf1` native file caching is preserved using a Docker volume (`fastf1_cache`) to avoid re-downloading large telemetry packets from external servers.
   - A Redis cache (`ProviderCache`) is introduced for high-level metadata caching.

## Consequences
- **Pros:** Total isolation between external data models and our internal Canonical Events. Scaling ingestion separately from normalization. Robust failure handling and replayability of raw fetches.
- **Cons:** More moving parts (two services instead of one monolithic ingestion script). Latency overhead due to intermediate Redis stream (negligible for our scale).
