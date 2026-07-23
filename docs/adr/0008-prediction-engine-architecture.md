# 8. Prediction Engine Architecture

Date: 2024-10-26

## Status
Accepted

## Context
PitWall AI requires a deterministic Prediction Engine capable of generating highly reproducible machine learning predictions using Canonical Events, independent of any generative AI or LLMs. This engine requires a unified registry for model metadata, standard feature pipelines, and distinct boundaries between real-time inference and offline training.

## Decision
1. **Framework Standardization:** We selected `scikit-learn` as the primary ML framework for this phase due to its speed, deterministic execution (with fixed random seeds), and built-in model calibration methods.
2. **Execution Separation:** 
   - **Offline Mode:** Feature engineering, model training, evaluation metrics, and backtesting execute via a CLI tool (`cli.py`), insulated from the real-time pipeline.
   - **Online Mode:** A FastAPI service backed by a Redis Consumer that loads `PRODUCTION` models from the registry and serves live predictions during a race.
3. **Model Registry:** Model metadata, hyper-parameters, versions, and validation metrics are stored in PostgreSQL via SQLAlchemy, allowing explicit model promotion (`STAGING` to `PRODUCTION`).

## Consequences
- **Pros:** Fast inference without bloated dependencies like PyTorch/TensorFlow where simple regressors suffice. Strict isolation between training latency and inference throughput. Full reproducibility.
- **Cons:** Feature pipelines must be meticulously kept in sync between the offline dataframe-based training and the online dict-based inference. If deep learning is needed later, the inference server dependency footprint will increase.
