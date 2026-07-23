# 10. Frontend and API Gateway Architecture

Date: 2024-10-26

## Status
Accepted

## Context
PitWall AI requires a high-performance, real-time user interface capable of streaming live telemetry while offering an integrated AI Chat and Strategy Workspace. The UI must also be secure, requiring authentication.

## Decision
1. **Frontend Framework:** Next.js (React) is chosen for the frontend due to its robust ecosystem and support for server/client boundaries. The UI uses Tailwind CSS for raw styling. State is managed by Zustand for simplicity and performance during high-frequency updates.
2. **API Gateway (FastAPI):** A new Python microservice (`api-gateway`) is introduced. This avoids tying the frontend directly to Redis or the backend services, enabling secure JWT authentication (via `POST /login`) and managed WebSocket connections (`GET /ws`).
3. **WebSocket Pub/Sub:** The API Gateway acts as a proxy, consuming protobuf events from the Redis `telemetry_group`, converting them to JSON, and broadcasting them to authenticated connected WebSocket clients.

## Consequences
- **Pros:** Full stack consistency (Python backend, React frontend). Secure access patterns. Next.js allows future SSR capabilities for historical sessions.
- **Cons:** Additional microservice (`api-gateway`) increases orchestration complexity. The WebSocket mapping from Protobuf to JSON requires maintenance if the proto schemas change significantly.
