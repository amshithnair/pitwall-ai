# 7. Strategy Engine Architecture

Date: 2024-10-26

## Status
Accepted

## Context
PitWall AI requires a central authority to compute optimal race strategies based on incoming telemetry and analytics, independently of any probabilistic AI models. This component needs to evaluate multiple potential pit window and tyre strategies dynamically and persist the recommendations.

## Decision
1. **Separation of Concerns:** The Strategy Engine is implemented as a standalone service, distinct from the Telemetry Engine.
2. **Deterministic Simulation:** We have opted to use static track baselines for tyre degradation and pit loss to maintain strict determinism, rather than deriving predictive curves on the fly. This guarantees reproducible outputs during 20x replays.
3. **Trigger Cadence:** Strategy re-evaluations occur deterministically upon the receipt of `analytics.lap` events, ensuring recommendations are strictly tied to completed physical race events rather than wall-clock time.
4. **Relational Persistence:** Unlike the Telemetry Engine (which uses TimescaleDB for time-series data), the Strategy Engine uses PostgreSQL via SQLAlchemy to store complex business entities like `StrategyRecommendation` for historical audits.

## Consequences
- **Pros:** Highly predictable, easily verifiable, isolated scaling, and clear separation of structured strategy state from raw time-series telemetry.
- **Cons:** Static baselines mean the engine does not "learn" if actual tyre degradation differs from the baseline in real-time (this will be handled by a future Predictive layer).
