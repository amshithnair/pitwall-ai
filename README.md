# PitWall AI

PitWall AI is an AI-native Formula 1 Intelligence Platform that transforms live and historical race data into engineering-grade insights through real-time analytics, predictive intelligence, and Large Language Models.

## Repository Structure

This repository follows a monorepo approach for all PitWall AI components:

- `docs/`: Product Requirements Document (PRD), Architecture Decision Records (ADRs).
- `services/`: Microservices (e.g., provider-adapter, normalizer, replay-engine, ai-orchestrator).
- `libs/`: Shared libraries (e.g., canonical event schemas).
- `frontend/`: The web application dashboard.

## Development

### Prerequisites
- Docker and Docker Compose
- Make (optional, but convenient shortcuts are provided)

### Environment Variables
Before running the application, you need to configure your environment variables. This project uses a `.env` file to securely pass configuration to Docker Compose.

1. Locate the `.env.example` file in the root directory.
2. Copy it to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open the `.env` file and insert your actual `OPENAI_API_KEY`. Without this, the AI Orchestrator will use a mock response.

### Quick Start

To build all the microservices and the Next.js frontend:
```bash
make build
# or run manually: docker-compose build
```

To start the foundational infrastructure (PostgreSQL, TimescaleDB, Redis, Qdrant) and all services:
```bash
make up
# or run manually: docker-compose up -d
```

> **Note on Timeouts:** If you experience a `TLS handshake timeout` while pulling images (like Qdrant or Postgres) via `make up`, this is a temporary network issue with Docker Hub. Retry the command, or pull the images individually first (`docker pull qdrant/qdrant:latest`).

### Accessing the Platform
Once running, you can access the following services:
- **Dashboard (Frontend):** `http://localhost:3000` (Login with username: `analyst`, password: `pitwall2024`)
- **API Gateway:** `http://localhost:8008`
- **AI Orchestrator:** `http://localhost:8007`

### Testing the Endpoints
You can use the provided PowerShell script to quickly verify that the API Gateway and AI Orchestrator are running properly.

```powershell
.\scripts\test_endpoints.ps1
```

To stop the infrastructure:
```bash
make down
```

## Documentation
- [Product Requirements Document (PRD)](docs/PRD.md)
- [Architecture Decision Records (ADRs)](docs/adr/README.md)
