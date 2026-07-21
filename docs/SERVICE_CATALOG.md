# Service Catalog

PitWall AI is composed of independently deployable microservices. Each service has a single, strictly bounded responsibility.

## Data Layer

### 1. Provider Adapter
- **Purpose**: Connects to external APIs or WebSockets (e.g., FastF1, Multiviewer).
- **Responsibilities**: Authenticates with providers, maintains persistent connections, receives provider-specific raw data.
- **Inputs**: External data feeds.
- **Outputs**: Raw Provider Events (internal to the ingestion pod).
- **Dependencies**: External Data Sources.
- **Failure Modes**: Disconnects from source. Should attempt exponential backoff and retry.
- **Scalability**: One instance per external provider stream.

### 2. Normalizer
- **Purpose**: Translates raw provider data into PitWall Canonical Events.
- **Responsibilities**: Schema validation, assigning UUIDs, enforcing monotonically increasing sequence numbers, packing Protocol Buffers.
- **Inputs**: Raw Provider Events.
- **Outputs**: Canonical Events (published to Redis Stream).
- **Dependencies**: Redis.
- **Failure Modes**: Unknown schema formats. Bad payloads must be logged and discarded, not crash the service.
- **Scalability**: Stateless; can be horizontally scaled if the stream is partitioned.

### 3. Replay Engine
- **Purpose**: Replays historical sessions as if they were live.
- **Responsibilities**: Reads historical Canonical Events from TimescaleDB and publishes them to Redis Streams at a configurable speed (1x, 5x, 20x).
- **Inputs**: TimescaleDB / PostgreSQL.
- **Outputs**: Canonical Events (published to Redis Stream).
- **Dependencies**: TimescaleDB, Redis.
- **Failure Modes**: Desync in high-speed replay. Must maintain strict event ordering.
- **Scalability**: One active replay instance per requested historical session.

### 4. Historical Loader
- **Purpose**: Backfills local databases with historical race metadata.
- **Responsibilities**: Connects to Ergast/Jolpica, pulls historical results, and populates the PostgreSQL relational DB.
- **Inputs**: External APIs.
- **Outputs**: SQL INSERTs to PostgreSQL.
- **Dependencies**: PostgreSQL.
- **Failure Modes**: Rate limiting from external APIs.

## Analytics Layer

### 5. Telemetry Engine
- **Purpose**: High-speed processing of raw telemetry.
- **Responsibilities**: Smoothing telemetry traces, calculating micro-sectors, detecting anomalies.
- **Inputs**: `telemetry.*` Canonical Events (from Redis Stream).
- **Outputs**: Derived Telemetry Events.
- **Dependencies**: Redis Stream.

### 6. Prediction Engine
- **Purpose**: Deterministic modeling of race outcomes.
- **Responsibilities**: Computes tyre degradation curves, safety car probabilities, and finishing position probabilities. NEVER generates natural language.
- **Inputs**: Canonical Events, Historical Data.
- **Outputs**: `prediction.generated` Canonical Events.
- **Dependencies**: TimescaleDB (for historical model context), Redis Stream.
- **Failure Modes**: Missing required inputs (e.g. weather data). Models must degrade gracefully and output lower confidence scores.

### 7. Strategy Engine
- **Purpose**: Calculates optimal race strategies.
- **Responsibilities**: Pit window calculation, undercut/overcut viability, fuel management.
- **Inputs**: `prediction.generated` events, Canonical Events.
- **Outputs**: `strategy.generated` Canonical Events.
- **Dependencies**: Redis Stream.

### 8. Weather Engine
- **Purpose**: Integrates meteorological data.
- **Responsibilities**: Normalizes radar and track temperature predictions.
- **Inputs**: OpenWeather / Meteostat data.
- **Outputs**: `weather.*` Canonical Events.

## Reasoning Layer

### 9. AI Orchestrator
- **Purpose**: Bridges the deterministic system with the Large Language Model.
- **Responsibilities**: Listens to the event stream, decides *when* an event warrants LLM invocation, retrieves RAG context, and constructs the LLM prompt.
- **Inputs**: Canonical Events (especially Prediction/Strategy), Qdrant (RAG).
- **Outputs**: Prompt payloads to the LLM Service.
- **Dependencies**: Qdrant, Redis Stream, LLM Service.
- **Failure Modes**: Excessive LLM invocation. Must enforce rate limits and debouncing.

### 10. LLM Service
- **Purpose**: Natural language generation and interaction.
- **Responsibilities**: Communicates with the upstream LLM API (e.g., Claude, Gemini). Returns plain text explanations.
- **Inputs**: Prompts from AI Orchestrator, User queries.
- **Outputs**: `ai.summary.generated`, `ai.insight.generated` Canonical Events.
- **Dependencies**: External LLM Provider API.
- **Failure Modes**: API timeouts, rate limits, high latency. Must implement fallback responses.

## Presentation Layer

### 11. API Gateway / WebSocket Server (Dashboard Service)
- **Purpose**: Serves the frontend clients.
- **Responsibilities**: WebSocket management, REST endpoints, Authentication (JWT), streaming Canonical Events to the browser.
- **Inputs**: HTTP Requests, Redis Streams.
- **Outputs**: HTTP Responses, WebSocket frames.
- **Dependencies**: Redis, PostgreSQL (for auth/sessions).
- **Scalability**: Highly concurrent. Should scale horizontally behind a load balancer.

### 12. Frontend
- **Purpose**: The user interface.
- **Responsibilities**: Rendering the F1TV/Bloomberg-style dashboard, rendering charts, managing AI chat.
- **Inputs**: WebSocket frames, HTTP Responses.
- **Outputs**: User interactions.
- **Dependencies**: API Gateway.
