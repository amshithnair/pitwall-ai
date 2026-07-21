# 0004. Separate Prediction Engine from AI Reasoning

* Status: accepted
* Deciders: Amshith Nair
* Date: 2026-07-21

Technical Story: Milestone 0.5 - AI Architecture

## Context and Problem Statement

The platform promises "AI-powered race analysis." Large Language Models (LLMs) are excellent at summarizing text and explaining concepts naturally. However, they are notoriously bad at performing complex deterministic math, physics modeling, and predicting outcomes based on raw high-frequency time-series data without hallucinating.

## Decision Drivers

* We must absolutely prevent hallucinations regarding race strategy or telemetry (e.g., inventing a pit stop or miscalculating tyre degradation).
* We need statistical confidence scores for predictions. LLMs cannot generate reliable mathematical confidence scores.
* Invoking an LLM on every telemetry tick is financially and computationally unfeasible.

## Considered Options

* Pass raw telemetry directly to the LLM and prompt it to predict strategy.
* Build a deterministic Prediction Engine that outputs structured JSON events, and have the LLM simply read those events to explain them.

## Decision Outcome

Chosen option: "Build a deterministic Prediction Engine that outputs structured JSON events, and have the LLM simply read those events to explain them", because it guarantees the mathematical correctness of predictions while leveraging the LLM exclusively for its strength: natural language explanation and synthesis.

### Positive Consequences

* Zero risk of mathematical hallucination in predictions.
* Predictions can be rigorously evaluated against historical ground truth using standard ML metrics (MAE, RMSE) before deployment.
* Massive cost savings by only invoking the LLM when the deterministic engine detects a "meaningful" event.

### Negative Consequences

* Increased architectural complexity (requires maintaining both traditional ML models in the Prediction Engine and prompt engineering in the AI Orchestrator).
