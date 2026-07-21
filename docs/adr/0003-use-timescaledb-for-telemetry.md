# 0003. Use TimescaleDB for Telemetry

* Status: accepted
* Deciders: Amshith Nair
* Date: 2026-07-21

Technical Story: Milestone 0.5 - Storage Architecture

## Context and Problem Statement

A single Formula 1 race generates millions of telemetry points (speed, throttle, brake, RPM, GPS coordinates at 10Hz for 20 cars over 2 hours). Storing this in a standard relational database table (e.g., standard PostgreSQL) will quickly lead to bloated indexes, slow inserts, and degraded query performance when the Prediction Engine attempts to train models across multiple historical seasons.

## Decision Drivers

* We need highly performant ingest rates for live telemetry.
* We need fast aggregation queries (e.g., "average track temp per lap").
* We want to minimize operational complexity by avoiding completely disparate database ecosystems if possible.
* We need an automated way to compress and retain massive amounts of old telemetry data.

## Considered Options

* Standard PostgreSQL
* TimescaleDB (PostgreSQL extension)
* InfluxDB
* ClickHouse

## Decision Outcome

Chosen option: "TimescaleDB", because it provides the time-series performance and automated chunking/compression of specialized databases like InfluxDB, but remains fully compatible with PostgreSQL. This allows us to JOIN time-series telemetry data with relational metadata (like Drivers and Circuits) in a single database connection using standard SQL.

### Positive Consequences

* Seamless integration with the existing PostgreSQL metadata layer.
* Automatic chunking via Hypertables ensures fast inserts regardless of table size.
* Native columnar compression saves massive amounts of disk space for historical races.
* Time-bucket functions (e.g., `time_bucket('1 second', timestamp)`) make smoothing telemetry traces trivial.

### Negative Consequences

* Requires managing the TimescaleDB extension and understanding Hypertable chunking intervals to optimize performance.
