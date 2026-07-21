# Canonical Event Model

## 1. Canonical Event Philosophy

The Canonical Event Schema is the central nervous system of PitWall AI. To guarantee service decoupling and data consistency across live races and historical replays, the platform adheres to a strict Canonical Event Philosophy:

- **Provider Agnosticism**: No downstream service (Analytics, Dashboard, LLM) is permitted to consume raw API responses from external data providers (e.g., FastF1, Multiviewer). All data must be normalized into the Canonical Event Schema.
- **Event-Driven Mutability**: System state changes exclusively in response to Canonical Events. There are no out-of-band updates.
- **Replay Parity**: Historical replays and live races emit structurally identical events. The consumer cannot distinguish between live ingestion and replay execution.

## 2. Event Lifecycle

1. **Ingestion**: A Provider Adapter receives external data (REST/WebSocket).
2. **Normalization**: The Adapter maps the external payload to a Canonical Event payload.
3. **Envelopment**: The Normalizer wraps the payload in the standard Event Envelope, assigning IDs, timestamps, and sequence numbers.
4. **Publishing**: The event is serialized (Protocol Buffers) and published to the central Redis Stream.
5. **Consumption**: Downstream services (Storage, Prediction, Dashboard) consume the stream asynchronously.

## 3. Event Versioning Policy

Events are versioned using a semantic `MAJOR.MINOR` scheme at the schema level.
- **Backward Compatibility**: Adding optional fields increments the `MINOR` version and does not break existing consumers.
- **Breaking Changes**: Removing fields or changing types increments the `MAJOR` version. Consumers must be migrated before deployment.
- **Multi-Version Support**: Replay engines ensure events are reconstructed in their original schema version to maintain historical accuracy.

## 4. The Event Envelope

Every event must be wrapped in this standard envelope.

```json
{
  "schema_version": "1.0",
  "event_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
  "event_type": "lap.completed",
  "session_id": "2026-bahrain-race",
  "race_id": "2026-bahrain",
  "driver_id": "VER",
  "timestamp": "2026-03-02T15:32:11.234Z",
  "sequence": 14823,
  "source": "fastf1",
  "payload": { ... }
}
```

### Constraints
- `timestamp`: Must be an ISO 8601 UTC string with millisecond precision.
- `sequence`: A monotonically increasing integer assigned by the Normalizer per `session_id` to guarantee ordering.
- `event_id`: A UUID v4 generated at creation time.
- `driver_id`: TLA (Three Letter Acronym) if applicable, otherwise omitted.

## 5. Event Categories & Definitions

### 5.1 Session Events
Events dictating the lifecycle of a race weekend session.
- **`session.started`**: Emitted when the session goes green.
- **`session.ended`**: Emitted when the session is officially closed.
  - *Producer*: Normalizer / Timing Provider
  - *Consumer*: All services (resets state)
  - *Payload Example*: `{"session_type": "Race", "laps_total": 57}`

### 5.2 Timing Events
Events related to lap and sector times.
- **`lap.started`**: Driver begins a new lap.
- **`lap.completed`**: Driver crosses the finish line.
  - *Payload Example*: `{"lap_number": 42, "lap_time_ms": 94231, "is_personal_best": true}`
- **`sector.completed`**: Driver completes a track sector.
  - *Producer*: Timing Provider
  - *Consumer*: Dashboard, Analytics, Prediction Engine

### 5.3 Position Events
Events tracking track position.
- **`position.changed`**: Driver moves up or down the classification.
  - *Producer*: Timing Provider
  - *Consumer*: Dashboard, Strategy Engine
  - *Payload Example*: `{"old_position": 4, "new_position": 3, "overtaken_driver_id": "NOR"}`

### 5.4 Pit Events
Events tracking pit lane activity.
- **`pit.entry`**: Driver crosses the pit entry line.
- **`pit.stop`**: The stationary phase of the pit stop.
  - *Payload Example*: `{"stationary_duration_ms": 2400}`
- **`pit.exit`**: Driver crosses the pit exit line.
  - *Producer*: Timing Provider
  - *Consumer*: Dashboard, Strategy Engine, AI Orchestrator

### 5.5 Tyre Events
Events tracking tyre compound usage and wear.
- **`tyre.changed`**: Emitted following a pit stop.
  - *Payload Example*: `{"compound": "HARD", "is_new": false, "stint_number": 2}`
- **`tyre.degradation`**: Emitted by the Prediction Engine based on telemetry wear models.
  - *Producer*: Prediction Engine
  - *Consumer*: Strategy Engine, AI Orchestrator

### 5.6 Telemetry Events
High-frequency vehicle state data.
- **`speed.updated`**, **`throttle.updated`**, **`brake.updated`**, **`drs.changed`**
  - *Producer*: Telemetry Provider
  - *Consumer*: Analytics Service, TimescaleDB Storage
  - *Payload Example*: `{"speed_kph": 321, "gear": 8, "rpm": 11500}`

### 5.7 Weather Events
Meteorological changes at the circuit.
- **`rain.started`**, **`weather.updated`**, **`track.temperature.changed`**
  - *Producer*: Weather Provider
  - *Consumer*: Strategy Engine, Prediction Engine, Dashboard
  - *Payload Example*: `{"air_temp_c": 28.5, "track_temp_c": 42.1, "rain_probability": 0.1}`

### 5.8 Race Control Events
Official FIA directives.
- **`safety_car.deployed`**, **`safety_car.ended`**
- **`virtual_safety_car.deployed`**, **`virtual_safety_car.ended`**
- **`red_flag`**, **`yellow_flag`**, **`green_flag`**
  - *Producer*: Race Control Provider
  - *Consumer*: Dashboard, Strategy Engine, AI Orchestrator

### 5.9 Prediction Events
Outputs from deterministic models in the Analytics Layer.
- **`prediction.generated`**
  - *Producer*: Prediction Engine
  - *Consumer*: Dashboard, AI Orchestrator
  - *Payload Example*: `{"prediction_type": "pit_window", "window_laps": [28, 30], "confidence": 0.82}`

### 5.10 Strategy Events
Outputs regarding optimal race strategies.
- **`strategy.generated`**
  - *Producer*: Strategy Engine
  - *Consumer*: Dashboard, AI Orchestrator

### 5.11 AI Events
Outputs from the reasoning layer.
- **`summary.generated`**, **`insight.generated`**
  - *Producer*: LLM Service
  - *Consumer*: Dashboard
  - *Payload Example*: `{"insight_text": "Norris is likely to stop between laps 28 and 30 due to high degradation on the medium compound."}`

### 5.12 System Events
Internal platform orchestration.
- **`service.health.failed`**, **`replay.started`**, **`replay.paused`**
  - *Producer*: System Orchestrators
  - *Consumer*: Monitoring, Dashboard
