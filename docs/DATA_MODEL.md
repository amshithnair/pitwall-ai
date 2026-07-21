# Data Model

The PitWall AI Data Model spans across three distinct storage engines based on the nature of the data: PostgreSQL (Relational Metadata), TimescaleDB (High-Frequency Time-Series), and Qdrant (Vector Embeddings).

## 1. Core Entities (PostgreSQL)

These entities represent the static and relational metadata surrounding a race weekend.

### `Season`
- **Fields**: `year` (INT), `url` (VARCHAR)
- **Primary Key**: `year`
- **Relationships**: 1:N with `GrandPrix`

### `Circuit`
- **Fields**: `circuit_id` (VARCHAR), `name` (VARCHAR), `location` (VARCHAR), `country` (VARCHAR), `length_meters` (INT)
- **Primary Key**: `circuit_id`
- **Relationships**: 1:N with `GrandPrix`

### `Constructor` (Team)
- **Fields**: `constructor_id` (VARCHAR), `name` (VARCHAR), `nationality` (VARCHAR)
- **Primary Key**: `constructor_id`

### `Driver`
- **Fields**: `driver_id` (VARCHAR), `code` (VARCHAR), `first_name` (VARCHAR), `last_name` (VARCHAR), `dob` (DATE), `nationality` (VARCHAR)
- **Primary Key**: `driver_id`

### `GrandPrix`
- **Fields**: `race_id` (VARCHAR), `year` (INT), `round` (INT), `circuit_id` (VARCHAR), `name` (VARCHAR), `date` (DATE)
- **Primary Key**: `race_id`
- **Relationships**: 1:N with `Session`

### `Session`
- **Fields**: `session_id` (VARCHAR), `race_id` (VARCHAR), `type` (ENUM: Practice 1, Practice 2, Practice 3, Qualifying, Sprint, Race), `start_time` (TIMESTAMPTZ)
- **Primary Key**: `session_id`

### `TyreSet`
- **Fields**: `tyre_set_id` (UUID), `session_id` (VARCHAR), `driver_id` (VARCHAR), `compound` (ENUM: SOFT, MEDIUM, HARD, INTER, WET), `is_new` (BOOLEAN), `stint_number` (INT)
- **Primary Key**: `tyre_set_id`

## 2. Race Execution Entities (TimescaleDB)

These entities are appended at high velocity and require time-series chunking.

### `Lap`
- **Fields**: `lap_id` (UUID), `session_id` (VARCHAR), `driver_id` (VARCHAR), `lap_number` (INT), `lap_time_ms` (INT), `timestamp` (TIMESTAMPTZ)
- **Primary Key**: `(session_id, driver_id, lap_number)`
- **Storage Engine**: TimescaleDB Hypertable
- **Retention**: Indefinite

### `Sector`
- **Fields**: `sector_id` (UUID), `lap_id` (UUID), `sector_number` (INT), `sector_time_ms` (INT), `timestamp` (TIMESTAMPTZ)
- **Storage Engine**: TimescaleDB Hypertable

### `Telemetry Point`
- **Fields**: `session_id` (VARCHAR), `driver_id` (VARCHAR), `timestamp` (TIMESTAMPTZ), `speed` (INT), `throttle` (INT), `brake` (INT), `gear` (INT), `rpm` (INT), `drs` (BOOLEAN), `x` (FLOAT), `y` (FLOAT), `z` (FLOAT)
- **Primary Key**: `(session_id, driver_id, timestamp)`
- **Storage Engine**: TimescaleDB Hypertable (chunked by day)
- **Retention**: Indefinite, heavily compressed using Timescale native compression after 7 days.

### `Weather Snapshot`
- **Fields**: `session_id` (VARCHAR), `timestamp` (TIMESTAMPTZ), `air_temp` (FLOAT), `track_temp` (FLOAT), `humidity` (FLOAT), `rain_probability` (FLOAT), `wind_speed` (FLOAT)
- **Storage Engine**: TimescaleDB Hypertable

### `Race Event`
- **Fields**: `event_id` (UUID), `session_id` (VARCHAR), `timestamp` (TIMESTAMPTZ), `event_type` (VARCHAR), `payload` (JSONB)
- **Storage Engine**: TimescaleDB Hypertable

### `Pit Stop`
- **Fields**: `pit_id` (UUID), `session_id` (VARCHAR), `driver_id` (VARCHAR), `lap_number` (INT), `duration_ms` (INT), `timestamp` (TIMESTAMPTZ)
- **Storage Engine**: TimescaleDB

## 3. Analytics & AI Entities (PostgreSQL / Qdrant)

### `Prediction`
- **Fields**: `prediction_id` (UUID), `session_id` (VARCHAR), `model_id` (VARCHAR), `model_version` (VARCHAR), `timestamp` (TIMESTAMPTZ), `prediction_type` (VARCHAR), `payload` (JSONB)
- **Storage Engine**: PostgreSQL (or TimescaleDB if high frequency)

### `Strategy Recommendation`
- **Fields**: `recommendation_id` (UUID), `session_id` (VARCHAR), `driver_id` (VARCHAR), `timestamp` (TIMESTAMPTZ), `payload` (JSONB)
- **Storage Engine**: PostgreSQL

### `AI Conversation`
- **Fields**: `conversation_id` (UUID), `session_id` (VARCHAR), `user_id` (VARCHAR), `created_at` (TIMESTAMPTZ)
- **Storage Engine**: PostgreSQL

### `RAG Embeddings` (Vector Store)
- **Fields**: `vector_id` (UUID), `embedding` (VECTOR), `metadata` (JSON)
- **Storage Engine**: Qdrant
- **Usage**: Used to retrieve historical events, strategy rules, or previous race analogies for the AI Orchestrator.

### `Replay Session`
- **Fields**: `replay_id` (UUID), `original_session_id` (VARCHAR), `speed_multiplier` (FLOAT), `current_timestamp` (TIMESTAMPTZ), `status` (ENUM: PLAYING, PAUSED, STOPPED)
- **Storage Engine**: Redis (Volatile State)
