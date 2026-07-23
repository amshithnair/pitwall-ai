# 9. AI Orchestrator Architecture

Date: 2024-10-26

## Status
Accepted

## Context
PitWall AI requires a reasoning layer capable of interpreting complex racing queries, retrieving rules, and orchestrating downstream service calls (Telemetry, Prediction, Strategy). This layer must bridge deterministic event systems with a conversational frontend.

## Decision
1. **Framework:** We chose LangGraph to orchestrate our F1 Engineering Agent. By utilizing `StateGraph` and `ToolNode`, we achieve a highly controllable, state-machine-driven execution loop that strictly utilizes the LLM as a planner and explainer.
2. **Provider Abstraction:** Provider-specific logic is isolated behind an `LLMProvider` interface. We use `OpenAIProvider` as the initial implementation, enabling easy swapping to local providers like Ollama without changing the LangGraph topology.
3. **RAG Vector Database:** We selected Qdrant as the vector store for its speed, simplicity, and excellent Python client support. It will host the FIA Sporting Regulations and historical race debriefs.
4. **Stateless API:** The `POST /chat` endpoint is intentionally stateless. Conversation history must be managed by the client or an API gateway. If persistent conversations are needed later, a dedicated Conversation Service backed by Redis or PostgreSQL will be introduced instead of coupling state management to the Orchestrator.

## Consequences
- **Pros:** LangGraph provides superior inspectability and determinism over standard LangChain agents. The `LLMProvider` interface prevents vendor lock-in. Stateless APIs simplify scaling.
- **Cons:** Dependent on external OpenAI APIs for baseline testing, which requires API keys. Future iterations will require implementing an `OllamaProvider` to satisfy strict air-gapped execution requirements.
