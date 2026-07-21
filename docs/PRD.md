# PitWall AI — Product Requirements Document

**Project:** PitWall AI
**Version:** 1.0.0
**Status:** Final Draft
**Author:** Amshith Nair
**Last Updated:** July 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Vision and Mission](#2-vision-and-mission)
3. [Problem Statement](#3-problem-statement)
4. [Product Goals](#4-product-goals)
5. [Target Audience](#5-target-audience)
6. [Data Acquisition Strategy](#6-data-acquisition-strategy)
7. [Canonical Event Schema](#7-canonical-event-schema)
8. [System Architecture](#8-system-architecture)
9. [Intelligence Layers](#9-intelligence-layers)
10. [Core Features](#10-core-features)
11. [Functional Requirements](#11-functional-requirements)
12. [Non-Functional Requirements](#12-non-functional-requirements)
13. [Storage Architecture](#13-storage-architecture)
14. [AI and LLM Capabilities](#14-ai-and-llm-capabilities)
15. [Prediction Engine](#15-prediction-engine)
16. [Validation and Evaluation Framework](#16-validation-and-evaluation-framework)
17. [LLM Cost Controls](#17-llm-cost-controls)
18. [Security](#18-security)
19. [Dashboard Philosophy](#19-dashboard-philosophy)
20. [Release Roadmap](#20-release-roadmap)
21. [Success Metrics](#21-success-metrics)
22. [Excluded from v1](#22-excluded-from-v1)
23. [Future Vision](#23-future-vision)
24. [Guiding Principles](#24-guiding-principles)

---

## 1. Executive Summary

PitWall AI is an AI-native Formula 1 Intelligence Platform that transforms live and historical race data into engineering-grade insights through real-time analytics, predictive intelligence, and Large Language Models.

Unlike traditional race dashboards that display telemetry, PitWall AI explains race strategy, predicts possible outcomes, and acts as an AI Race Engineer capable of answering complex questions in natural language.

The platform is built on three separations of concern that are non-negotiable:

- A **Data Layer** that acquires, normalizes, and stores race data as canonical versioned events.
- An **Analytics Layer** that performs deterministic calculations, physics models, and predictive simulations.
- A **Reasoning Layer** where the LLM consumes structured outputs from the Analytics Layer and provides explanations, summaries, and conversational interaction.

The LLM never performs predictions. The prediction engine never hallucinates. The data layer never leaks provider-specific formats into downstream services.

---

## 2. Vision and Mission

**Vision**

> Build the most intelligent Formula 1 race analysis platform available outside professional motorsport teams.

**Mission**

To provide an engineering-grade Formula 1 intelligence platform capable of ingesting race events, understanding race context, reasoning over historical knowledge, and assisting users through conversational AI that explains rather than fabricates.

**Motto**

> PitWall AI doesn't just tell you what happened. It tells you why it happened — and what is likely to happen next.

---

## 3. Problem Statement

Formula 1 data is fragmented across multiple platforms: live timing, weather, race control, telemetry, driver radio, historical archives, and strategy discussions. Users switch between multiple websites to understand a race. Even then, they only see *what* happened — rarely *why*.

PitWall AI consolidates all race intelligence into one platform powered by AI that explains, not just displays.

---

## 4. Product Goals

**Primary**

- Build a real-time Formula 1 intelligence platform.
- Provide AI-powered race analysis grounded in deterministic outputs.
- Visualize race telemetry professionally.
- Create an engineering-focused dashboard inspired by F1TV and Bloomberg Terminal.
- Develop a production-grade AI system suitable for long-term expansion.

**Secondary**

- Showcase distributed systems and event-driven architecture.
- Demonstrate production-ready backend with observable, independently deployable services.
- Build a validatable prediction system with real accuracy metrics.
- Serve as an engineering portfolio demonstrating AI, backend, and infrastructure skills.

---

## 5. Target Audience

**Primary Users**

- Formula 1 fans who want to understand strategy, tyres, weather, and driver performance without switching between multiple websites.
- Motorsport engineers and data analysts.
- Engineering students learning race strategy, telemetry, and AI reasoning.
- Software engineers evaluating the architecture.

**Secondary Users**

- Technical recruiters evaluating backend engineering, AI systems, cloud infrastructure, and product design.
- Content creators, journalists, and researchers.

---

## 6. Data Acquisition Strategy

Data sourcing is the single largest risk to PitWall AI. Without reliable data, no other feature exists. This section defines sources, risks, and the architectural principle that governs all data ingestion.

### 6.1 Data Source Registry

| Data | Source | Stability |
|---|---|---|
| Historical Results | Jolpica (Ergast successor) | Stable |
| Historical Sessions | FastF1 | Stable |
| Live Timing | FastF1 Live Timing / Multiviewer ecosystem | Experimental |
| Weather | OpenWeather or Meteostat | Stable |
| Circuit Metadata | Static dataset | Stable |
| Driver and Team Metadata | Static dataset | Stable |
| AI Knowledge | Internal RAG corpus | Stable |

### 6.2 Known Risks

- Official Formula 1 APIs are not publicly available.
- Live timing sources are unofficial and may change or break without notice.
- Licensing restrictions may prevent redistribution of data.
- The platform must degrade gracefully if live timing is unavailable.

### 6.3 Architectural Principle: Provider Abstraction

> The platform must never depend on a single external data provider.

Every provider implements the same ingestion interface. Replacing a provider must not affect any downstream service.

```python
class TimingProvider:
    async def connect(self) -> None: ...
    async def get_session(self, session_id: str) -> Session: ...
    async def stream_events(self) -> AsyncIterator[RawEvent]: ...
```

The ingestion pipeline is:

```
External Source
      │
      ▼
Provider Adapter (implements TimingProvider)
      │
      ▼
Normalizer (converts to Canonical Event)
      │
      ▼
Redis Streams
      │
      ▼
All Downstream Services
```

### 6.4 Replay-First Development

The platform is not designed around live races. Every race is represented as a replayable event stream.

```
Historical Race Data
        │
        ▼
Replay Engine
        │
        ├── 1× (real-time)
        ├── 5× (accelerated)
        └── 20× (batch)
        │
        ▼
Canonical Event Stream
        │
        ▼
Identical to Live Pipeline
```

Every service — dashboard, prediction engine, AI, storage — consumes the same event stream regardless of whether the data is historical or live. When live ingestion is ready, it becomes another producer feeding the same event model. This is not a testing convenience — it is the core development strategy.

---

## 7. Canonical Event Schema

The event schema is the foundation of PitWall AI. It is non-negotiable, versioned, and immutable once published.

### 7.1 Design Principle

> Every race is represented as a stream of versioned domain events. Every service speaks only this format. No service consumes raw API responses or provider-specific formats.

### 7.2 Event Envelope

Every event carries a common envelope regardless of type.

```json
{
  "schema_version": "1.0.0",
  "event_id": "uuid-v4",
  "event_type": "lap.completed",
  "session_id": "2025-bahrain-race",
  "race_id": "2025-bahrain",
  "driver_id": "VER",
  "timestamp": "2025-03-02T15:32:11.234Z",
  "sequence": 14823,
  "source": "fastf1",
  "payload": {}
}
```

The `payload` schema is defined per `event_type`. The envelope fields are identical for every event.

### 7.3 Event Type Registry

**Session**
- `session.started`
- `session.ended`

**Timing**
- `lap.started`
- `lap.completed`
- `sector.completed`

**Position**
- `position.changed`

**Pit**
- `pit.entry`
- `pit.stop`
- `pit.exit`

**Tyres**
- `tyre.changed`
- `tyre.degradation`

**Weather**
- `rain.started`
- `track.temperature.changed`
- `weather.updated`

**Race Control**
- `safety_car.deployed`
- `safety_car.ended`
- `virtual_safety_car.deployed`
- `virtual_safety_car.ended`
- `red_flag`
- `yellow_flag`
- `green_flag`

**Telemetry**
- `speed.updated`
- `throttle.updated`
- `brake.updated`
- `drs.changed`

**AI System**
- `prediction.generated`
- `strategy.generated`
- `summary.generated`

### 7.4 Serialization

Canonical events are serialized as Protocol Buffers for the following reasons:

- Schema evolution with backward compatibility.
- Strong typing enforced at compile time.
- Smaller payloads than JSON.
- Easier multi-language service support.
- Better replay compatibility across versions.

Every schema change increments the version and ships with migration tooling. Historical events remain reproducible in their original schema version.

---

## 8. System Architecture

### 8.1 High-Level Service Map

```
Data Sources
     │
     ▼
Provider Adapters
     │
     ▼
Normalizer
     │
     ▼
Redis Streams (Canonical Event Bus)
     │
     ├──► Replay Engine
     ├──► Dashboard Service (WebSocket → Frontend)
     ├──► Prediction Engine
     ├──► Historical Storage (TimescaleDB + PostgreSQL)
     ├──► AI Orchestrator
     │         │
     │         └──► LLM (Claude Sonnet via API)
     └──► Analytics Service
```

### 8.2 Service Responsibilities

| Service | Responsibility |
|---|---|
| Provider Adapter | Connects to external source, emits raw events |
| Normalizer | Converts raw events to canonical envelope |
| Replay Engine | Replays historical event streams at configurable speed |
| Dashboard Service | Streams real-time state to frontend via WebSocket |
| Prediction Engine | Deterministic models: tyres, pit windows, pace, safety car |
| Analytics Service | Calculations, comparisons, stint analysis |
| AI Orchestrator | Decides when to invoke LLM; assembles context |
| LLM Service | Explanation, summarization, conversational QA |
| Historical Storage | Persistent storage of all events and derived state |

Every service is independently deployable and containerized.

---

## 9. Intelligence Layers

There are exactly three intelligence layers. Their boundaries are enforced at the architecture level.

### Layer 1 — Data Layer

Acquires, normalizes, validates, and stores all race data.

Outputs: Canonical events on Redis Streams.

Does not reason. Does not predict.

### Layer 2 — Analytics Layer

Performs all deterministic calculations, physics models, simulations, and predictions.

Inputs: Canonical events and historical data.

Outputs: Structured JSON with model version metadata.

```json
{
  "prediction_type": "pit_window",
  "driver_id": "NOR",
  "window_laps": [28, 30],
  "confidence": 0.82,
  "model_version": "tyre-v1.2",
  "model_trained_on": "2024-seasons",
  "evaluated_at": "2025-01-15"
}
```

Does not generate language. Does not communicate with users.

### Layer 3 — Reasoning Layer

The LLM consumes structured outputs from Layer 2 and responds in natural language.

Inputs: Structured prediction outputs, session context, historical RAG corpus.

Outputs: Natural language explanations, summaries, conversational answers.

Does not receive raw telemetry. Does not invent confidence scores.

```
Telemetry
    │
    ▼
Prediction Engine (Layer 2)
    │
    ▼
Structured Output: { pit_window: [28,30], confidence: 0.82 }
    │
    ▼
LLM (Layer 3): "Norris is likely to stop between laps 28 and 30..."
```

**The LLM is never responsible for predictions. The prediction engine is never responsible for language.**

---

## 10. Core Features

### 10.1 Race Dashboard

Displays live or replayed:

- Driver positions, gaps, and intervals
- Lap times and sector splits
- Stint and tyre information
- Track status (Safety Car, VSC, red flag, yellow)
- Weather conditions

### 10.2 Driver Workspace

Dedicated engineering view per driver.

Contains:

- Position, speed, pace graph
- Lap history and sector comparison
- Tyre compound, age, and degradation estimate
- Fuel estimate
- Historical comparison against previous seasons

### 10.3 AI Race Engineer

Natural language assistant grounded in Layer 2 outputs.

Example queries:

- Why did Ferrari pit when they did?
- Compare Verstappen and Norris on medium tyres in sector two.
- What is the likely remaining race strategy for Piastri?
- Explain why tyre degradation increased in the last five laps.
- What happened at the 2023 Monaco Grand Prix?

The AI provides explanations, not raw statistics. All predictions cited in AI responses originate from the Analytics Layer with documented model versions.

### 10.4 Strategy Center

Powered by the Analytics Layer, displayed in the UI with LLM explanations.

- Pit window prediction per driver
- Undercut and overcut simulator
- Tyre degradation curves
- Fuel estimation
- Weather impact modeling
- Position prediction under different strategy assumptions

### 10.5 Historical Explorer

Searchable Formula 1 knowledge base backed by RAG.

Examples:

- Every Monaco Safety Car since 2010
- Ferrari average pit stop time by circuit
- Verstappen's pace profile on hard tyres
- Hungary race strategy 2023

### 10.6 Live AI Insights

The AI Orchestrator surfaces proactive insights when meaningful events occur — not continuously.

Example output:

```
Pit Window Opening

Driver: Oscar Piastri
Confidence: 91% (tyre-v1.2, validated MAE: 1.1 laps)

Tyre degradation has crossed the threshold model.
Traffic window is clear ahead.
Rain probability remains below 15%.
```

Confidence scores shown in the UI are always sourced from validated models with documented accuracy.

### 10.7 Race Timeline

Chronological visualization of:

- Pit stops
- Overtakes and position changes
- Safety Car and flag events
- Weather changes
- Strategy changes

### 10.8 Model Performance Dashboard

Internal view (and public showcase) of prediction model accuracy over historical races.

- Pit window MAE
- Tyre degradation RMSE
- Safety car Brier score
- Per-race accuracy breakdowns

---

## 11. Functional Requirements

The platform shall:

- Replay historical race sessions as canonical event streams.
- Accept live timing via provider adapters without changing downstream services.
- Stream dashboard updates to connected clients via WebSocket.
- Store all canonical events persistently.
- Generate AI summaries grounded in structured analytics outputs.
- Run driver comparisons using Analytics Layer calculations.
- Predict race events using versioned, validated models.
- Search historical races via the RAG knowledge base.
- Maintain user sessions with JWT authentication.
- Evaluate prediction model performance against historical ground truth.
- Prevent model promotion unless predefined accuracy thresholds are met.

---

## 12. Non-Functional Requirements

**Performance**

- Dashboard updates delivered within 500ms.
- AI responses generated within 5 seconds.
- Replay engine supports 1×, 5×, and 20× speed without dropping events.

**Availability**

- 99% uptime target.
- Graceful degradation if live timing source is unavailable.
- Automatic recovery after service failures.

**Scalability**

- Supports thousands of concurrent WebSocket connections.
- Multiple race sessions simultaneously.
- AI inference queue management to prevent overload.

**Observability**

- Prometheus metrics.
- Grafana dashboards.
- OpenTelemetry distributed tracing.
- Loki log aggregation.
- Every service emits structured logs and spans.

**Reliability**

- All canonical events are persisted before any downstream processing.
- Persistent storage with backup strategy.

---

## 13. Storage Architecture

Three distinct workloads require three distinct storage engines.

| Workload | Technology | Rationale |
|---|---|---|
| Relational metadata (sessions, drivers, circuits, teams) | PostgreSQL | Standard relational model, strong consistency |
| High-frequency telemetry (speed, throttle, brake, position) | TimescaleDB | PostgreSQL extension with hypertables, compression, retention, time-series functions |
| AI embeddings (RAG knowledge corpus) | Qdrant | Purpose-built vector store |
| Event streaming and cache | Redis Streams + Redis Cache | Sub-millisecond pub/sub and response caching |

**TimescaleDB is required.** Treating telemetry at 100ms cadence across a full race session as ordinary relational data will cause query performance failures as analytical patterns grow. TimescaleDB provides hypertable partitioning, automatic compression, and time-bucket aggregation within the familiar PostgreSQL ecosystem.

---

## 14. AI and LLM Capabilities

The LLM must:

- Accept structured inputs from the Analytics Layer, not raw telemetry.
- Explain race strategies in accessible natural language.
- Summarize sessions, stints, and strategic moments.
- Compare drivers using calculated metrics, not intuition.
- Answer historical questions via RAG retrieval.
- Attribute predictions to the model that produced them.

The LLM must not:

- Generate confidence scores or numerical predictions.
- Receive raw telemetry directly.
- Summarize the same event repeatedly within a debounce window.
- Be invoked on a timer or continuous basis.

**AI correctness takes priority over creativity.** When the analytics data does not support a claim, the LLM should say so rather than speculate.

---

## 15. Prediction Engine

The Prediction Engine is a separate service in the Analytics Layer. It never uses an LLM internally.

### 15.1 Models

| Model | Inputs | Output |
|---|---|---|
| Tyre Degradation | Compound, age, track temp, speed trace | Degradation rate curve |
| Pit Window | Degradation curve, track position, traffic | Optimal stop lap range |
| Pace Trend | Sector times, fuel load estimate | Expected lap time evolution |
| Safety Car Probability | Incident rate history, circuit, lap number | Per-lap probability |
| Weather Impact | Forecast, track temp, track temp, rain probability | Delta lap time estimate |
| Finishing Position | All of the above | Probability distribution |

### 15.2 Model Registry

Every prediction carries provenance metadata.

```json
{
  "model_id": "tyre-degradation",
  "model_version": "1.2.0",
  "trained_on": "2023-2024-seasons",
  "evaluation_date": "2025-01-15",
  "validation_metrics": {
    "rmse": 0.041,
    "mae": 0.029
  }
}
```

Historical predictions remain reproducible. When a model is retrained, older predictions reference the version that generated them.

---

## 16. Validation and Evaluation Framework

This is a dedicated milestone, not an afterthought. No prediction model is exposed in the UI before it has passed validation.

### 16.1 Evaluation Pipeline

```
Historical Race
      │
      ▼
Replay Engine (20× speed)
      │
      ▼
Prediction Engine
      │
      ▼
Predictions with Timestamps
      │
      ▼
Ground Truth Loader
      │
      ▼
Evaluator
      │
      ▼
Accuracy Reports + Calibration Curves
```

### 16.2 Metrics by Model

**Pit Window Prediction**
- Mean Absolute Error (laps)
- Accuracy within ±1 lap
- Accuracy within ±2 laps

**Tyre Degradation**
- RMSE
- MAE
- Trend correlation coefficient

**Safety Car Probability**
- Brier Score
- ROC-AUC
- Precision and Recall at threshold

**Finishing Position**
- Top-1 accuracy
- Top-3 accuracy
- Kendall Tau rank correlation

### 16.3 Promotion Gate

A model is only deployed to production when it meets predefined thresholds across a minimum number of historical race sessions. Thresholds are documented and version-controlled alongside the model code.

The confidence score shown to users is always derived from validation results, never asserted by the model itself.

---

## 17. LLM Cost Controls

Continuous LLM invocation during a live race is not acceptable architecturally or economically.

### 17.1 AI Orchestrator

The Orchestrator sits between the event stream and the LLM. It decides whether an event warrants LLM invocation.

```
Canonical Event Stream
        │
        ▼
Event Classifier (deterministic rules)
        │
        ├── Meaningful? → YES → Assemble Context → LLM
        └── Meaningful? → NO  → Ignore
```

**Trigger conditions (examples)**

- Safety Car deployed or ended
- Driver enters pit lane
- Rain probability crosses 30% threshold
- Tyre wear exceeds degradation model threshold
- Strategy divergence detected between top-4 drivers
- Race finish

Everything else is handled by deterministic logic with no LLM invocation.

### 17.2 Caching and Debouncing

- Redis response cache — identical context hashes return cached response.
- Prompt cache — system prompt cached at provider level.
- Embedding cache — RAG results cached per query.
- Debounce window — same event category cannot trigger LLM within N seconds.
- User-specific rate limits — prevents runaway usage per session.

---

## 18. Security

### 18.1 MVP (Milestone 1)

- JWT authentication with refresh tokens.
- Session management.
- HTTPS enforced everywhere.
- CORS policy.
- Rate limiting on API and WebSocket connections.
- Secrets managed via environment variables or Vault.

### 18.2 Production (Milestone 6)

- OAuth 2.0 provider integration.
- RBAC for multi-user access.
- API key management.
- Audit logs.
- Fine-grained permissions.

---

## 19. Dashboard Philosophy

The UI should resemble a professional engineering workstation, not a consumer application.

**Design inspiration:** F1TV Live Timing, Bloomberg Terminal, Mission Control, Grafana, modern IDEs.

**Characteristics:**

- Dark theme.
- Information-dense with deliberate whitespace.
- Modular and resizable panels.
- Fast — every interaction is instant or shows progress.
- Keyboard-friendly navigation.
- Minimal decoration; data is the primary visual element.

---

## 20. Release Roadmap

### Milestone 0 — Foundation

- Repository structure.
- ADR (Architecture Decision Record) framework.
- Documentation templates.
- Revised PRD finalized.
- Development environment definition.

### Milestone 1 — Infrastructure

- Docker Compose for all services.
- PostgreSQL, TimescaleDB, Redis, Qdrant provisioned.
- JWT authentication service.
- Backend API scaffold (FastAPI or equivalent).
- Frontend scaffold with WebSocket support.
- CI/CD pipeline.

### Milestone 2 — Data Layer

- Canonical event schema defined and compiled (protobuf).
- Historical data ingestion via FastF1 adapter.
- Normalizer service.
- Event persistence to TimescaleDB.
- Jolpica adapter for race metadata.
- Data validation and schema enforcement.

### Milestone 3 — Replay Engine and Dashboard

- Replay Engine with configurable speed (1×, 5×, 20×).
- WebSocket streaming from Redis Streams to frontend.
- Race Dashboard with live timing table.
- Driver Workspace basic view.
- Race Timeline.

### Milestone 3.5 — Validation Framework

- Evaluation pipeline scaffolded.
- Baseline metrics collected for tyre and pit models.
- Model Registry implemented.
- Promotion gate logic for models.
- Accuracy reports generated for at least one full season.

### Milestone 4 — Prediction Engine

- Tyre degradation model.
- Pit window model.
- Pace trend model.
- Safety car probability model.
- Strategy Center UI connected to Analytics Layer.
- All predictions validated before UI exposure.

### Milestone 5 — AI Race Engineer

- RAG knowledge corpus ingestion.
- Qdrant embeddings indexed.
- AI Orchestrator with trigger logic.
- LLM integration with structured context assembly.
- Natural language QA in UI.
- Live AI Insights panel with event-triggered insights.
- Historical Explorer powered by RAG.

### Milestone 6 — Production Hardening

- Observability stack (Prometheus, Grafana, Loki, OpenTelemetry).
- OAuth integration.
- RBAC.
- Load testing.
- Documentation coverage.
- Production deployment.
- Model performance dashboard in UI.

---

## 21. Success Metrics

**Technical**

- Dashboard latency consistently under 500ms.
- Replay engine stable at 20× without event loss.
- AI response within 5 seconds.
- Pit window MAE below 2 laps across validation set.
- WebSocket infrastructure stable under concurrent load.

**User**

- One dashboard replaces multiple websites.
- AI explanations are understandable to a non-engineer.
- Users can analyze a complete race without external resources.
- Confidence scores match documented model accuracy.

**Engineering**

- Every service independently deployable.
- Every prediction traceable to a model version.
- Full CI/CD with automated tests.
- Documentation covers all services, events, and models.
- No model promoted without passing validation gate.

---

## 22. Excluded from v1

- Video streaming.
- Team radio audio playback.
- Betting or fantasy integration.
- Mobile application.
- Multi-sport support (planned for v2).
- OAuth and RBAC (MVP uses JWT only).

---

## 23. Future Vision

PitWall AI should evolve into a multi-series motorsport intelligence platform.

**Target series (post-v1)**

- Formula 2
- Formula E
- WEC
- IndyCar
- IMSA
- MotoGP

The architecture supports this because only the Provider Adapter layer changes between championships. The canonical event schema, Analytics Layer, LLM integration, and storage architecture remain unchanged. Adding a new series means writing one new adapter and extending the event type registry where necessary.

---

## 24. Guiding Principles

**AI should explain, not hallucinate.**
The LLM only speaks from structured, validated inputs. When it does not know, it says so.

**Predictions must be measurable.**
A confidence score is only credible when backed by documented validation metrics. Every model carries its accuracy history.

**The event schema is the contract.**
No service communicates outside the canonical event format. Provider details never leak downstream.

**Replay is the primary development environment.**
Features are built and tested against historical replays. Live timing is an input variant, not a special case.

**Engineering quality takes priority over rapid feature delivery.**
Every service is observable, independently deployable, and documented.

**Documentation is part of the product.**
Architecture decisions are recorded. Model training and validation are documented. APIs are specified before implementation.

**Production readiness is a requirement, not an afterthought.**
Monitoring, alerting, graceful degradation, and cost controls are designed in from Milestone 1.
