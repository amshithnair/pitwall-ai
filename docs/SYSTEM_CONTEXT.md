# System Context (C4 Model)

This document describes the high-level architecture of PitWall AI using the C4 model concepts (Context & Containers).

## 1. System Context Diagram

```mermaid
C4Context
    title System Context for PitWall AI

    Person(user, "F1 Fan / Engineer", "Interacts with the dashboard to understand race strategy and telemetry.")
    
    System(pitwall, "PitWall AI", "Provides real-time engineering-grade insights, predictions, and conversational AI for Formula 1 races.")
    
    System_Ext(f1_live, "F1 Live Timing", "Unofficial real-time telemetry and timing feed.")
    System_Ext(jolpica, "Jolpica (Ergast)", "Historical race results and metadata.")
    System_Ext(weather, "OpenWeather", "Meteorological data.")
    System_Ext(llm, "LLM Provider", "Claude / Gemini API for natural language generation.")

    Rel(user, pitwall, "Views dashboard, asks AI questions")
    Rel(pitwall, f1_live, "Consumes live telemetry (WebSocket)")
    Rel(pitwall, jolpica, "Fetches historical results (REST)")
    Rel(pitwall, weather, "Fetches weather forecasts (REST)")
    Rel(pitwall, llm, "Sends structured prompts, receives natural language (REST)")
```

## 2. Container Diagram

```mermaid
C4Container
    title Container Diagram for PitWall AI

    Person(user, "F1 Fan / Engineer", "Uses the web interface.")

    System_Boundary(c1, "PitWall AI") {
        Container(spa, "Web Dashboard", "React / Vue", "Provides the user interface, renders charts, handles chat.")
        
        Container(api_gw, "API Gateway & WebSocket", "FastAPI / Node", "Handles client connections, JWT auth, and streams events.")
        
        Container(normalizer, "Ingestion & Normalizer", "Python", "Connects to external feeds and normalizes data into Canonical Events.")
        
        Container(replay, "Replay Engine", "Go / Python", "Streams historical events at configured speeds.")
        
        Container(prediction, "Analytics & Prediction Engine", "Python", "Runs deterministic models for tyre wear, pit windows, etc.")
        
        Container(ai_orch, "AI Orchestrator", "Python", "Determines when to invoke the LLM and builds the prompt context.")
        
        ContainerDb(redis, "Event Bus & Cache", "Redis Streams", "Central nervous system for canonical events.")
        
        ContainerDb(timescale, "Telemetry DB", "TimescaleDB", "Stores high-frequency telemetry and events.")
        
        ContainerDb(postgres, "Metadata DB", "PostgreSQL", "Stores static metadata, users, sessions.")
        
        ContainerDb(qdrant, "Vector DB", "Qdrant", "Stores RAG embeddings for historical context.")
    }

    System_Ext(external_data, "Data Providers", "FastF1, Jolpica, Weather")
    System_Ext(llm, "LLM Provider", "Claude / Gemini")

    Rel(user, spa, "Uses", "HTTPS")
    Rel(spa, api_gw, "Connects to", "WSS / HTTPS")
    Rel(api_gw, redis, "Subscribes to events", "TCP")
    
    Rel(normalizer, external_data, "Ingests raw data", "WSS / HTTPS")
    Rel(normalizer, redis, "Publishes Canonical Events", "TCP")
    
    Rel(replay, timescale, "Reads historical events", "TCP")
    Rel(replay, redis, "Publishes Canonical Events", "TCP")
    
    Rel(prediction, redis, "Consumes events & Publishes predictions", "TCP")
    Rel(prediction, timescale, "Reads historical model data", "TCP")
    
    Rel(ai_orch, redis, "Consumes predictions", "TCP")
    Rel(ai_orch, qdrant, "Retrieves RAG context", "TCP")
    Rel(ai_orch, llm, "Invokes LLM API", "HTTPS")
    Rel(ai_orch, redis, "Publishes AI summaries", "TCP")
    
    Rel(normalizer, timescale, "Persists all events", "TCP")
```

## 3. Data Movement Summary

1. **Ingestion**: The Normalizer pulls from `external_data`.
2. **Translation**: Normalizer converts to protobuf Canonical Events and pushes to `redis` streams.
3. **Persistence**: A dedicated worker reads from `redis` and writes to `timescale` and `postgres`.
4. **Analytics**: The Prediction Engine reads from `redis`, computes deterministically, and writes prediction events back to `redis`.
5. **Reasoning**: The AI Orchestrator listens to `redis` for prediction events. If a threshold is met, it queries `qdrant` for context, calls the `llm`, and writes an AI summary event back to `redis`.
6. **Presentation**: The API Gateway subscribes to `redis` and pushes all relevant events via WebSocket to the `spa`.
