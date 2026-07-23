# 9. AI Orchestrator Architecture

Date: 2024-10-26

## Status
Accepted

## Context
PitWall AI requires a reasoning layer capable of interpreting complex racing queries, retrieving rules, and orchestrating downstream service calls (Telemetry, Prediction, Strategy). This layer must bridge deterministic event systems with a conversational frontend.

## Decision
1. **Framework:** We chose LangChain in conjunction with `langchain-openai` for its robust function-calling (Tool) ecosystem, making it trivial to bind our Python APIs to the LLM.
2. **RAG Vector Database:** We selected Qdrant as the vector store for its speed, simplicity, and excellent Python client support. It will host the FIA Sporting Regulations and historical race debriefs.
3. **Stateless API:** The `POST /chat` endpoint is intentionally stateless. Conversation history must be managed by the client or an API gateway. This prevents the Orchestrator from needing complex distributed session management using Redis immediately, keeping the focus on reasoning and retrieval.

## Consequences
- **Pros:** Fast implementation time, highly extensible Tool array (we can easily add `get_weather` or `get_lap_times`), and easy testing through mock tools.
- **Cons:** Dependent on external OpenAI APIs for baseline testing, which requires API keys. Future iterations may require an air-gapped fallback using Ollama or vLLM to satisfy strict deterministic and on-premise execution requirements.
