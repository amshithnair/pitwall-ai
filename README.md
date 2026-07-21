# PitWall AI

PitWall AI is an AI-native Formula 1 Intelligence Platform that transforms live and historical race data into engineering-grade insights through real-time analytics, predictive intelligence, and Large Language Models.

## Repository Structure

This repository follows a monorepo approach for all PitWall AI components:

- `docs/`: Product Requirements Document (PRD), Architecture Decision Records (ADRs).
- `services/`: Microservices (e.g., normalizer, replay-engine, ai-orchestrator).
- `libs/`: Shared libraries (e.g., canonical event schemas).
- `frontend/`: The web application dashboard.

## Development

### Prerequisites
- Docker and Docker Compose
- Make

### Quick Start
To start the foundational infrastructure (PostgreSQL, TimescaleDB, Redis, Qdrant):
```bash
make up
```

To stop the infrastructure:
```bash
make down
```

## Documentation
- [Product Requirements Document (PRD)](docs/PRD.md)
- [Architecture Decision Records (ADRs)](docs/adr/README.md)
