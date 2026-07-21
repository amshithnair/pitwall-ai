# AI Architecture

PitWall AI enforces a strict architectural boundary between **Deterministic Analytics** and **AI Reasoning**. Large Language Models (LLMs) are exceptional at summarization, explanation, and contextualization, but they are unreliable at mathematical computation and physics modeling.

**The LLM never generates raw predictions. The Prediction Engine never generates natural language.**

## 1. Separation of Concerns

### Analytics & Prediction Engine (Deterministic)
- **Tooling**: Python, NumPy, SciPy, scikit-learn.
- **Responsibilities**: Calculating tyre degradation curves, computing pit window lap ranges, evaluating safety car probabilities.
- **Outputs**: Structured Canonical Events (JSON/Protobuf) containing numerical predictions and statistically validated confidence scores.
- **Hallucination Risk**: Zero.

### AI Orchestrator & LLM Service (Reasoning)
- **Tooling**: Claude 3.5 Sonnet / Gemini 1.5 Pro, Qdrant (Vector DB), LangChain/LlamaIndex.
- **Responsibilities**: Reading the deterministic predictions, querying historical RAG data, and explaining *why* the prediction is what it is in natural language.
- **Outputs**: Natural language text mapped to AI Canonical Events.
- **Hallucination Risk**: Mitigated by strict grounding in structured data.

## 2. Event-Driven Invocation

To control costs and prevent spam, the LLM is **not** invoked continuously. It is triggered by the AI Orchestrator based on specific event thresholds.

### Trigger Examples:
- `prediction.generated` where `confidence > 0.85` and `prediction_type == "pit_window_open"`.
- `tyre.degradation` event crossing the critical drop-off threshold.
- `safety_car.deployed` event.

### Debouncing & Caching
- **Debounce**: If a `safety_car.deployed` event triggers an LLM summary, subsequent safety car updates are ignored for N minutes unless the state changes significantly.
- **Semantic Caching**: Common queries (e.g., "What is a virtual safety car?") hit a Redis semantic cache before reaching the LLM provider.

## 3. RAG and Embeddings

When the AI Orchestrator triggers an LLM invocation, it enriches the prompt using Retrieval-Augmented Generation (RAG).

- **Corpus**: Historical race summaries, technical regulations, circuit overtaking difficulty metrics, tyre compound characteristics.
- **Vector Store**: Qdrant.
- **Process**: 
  1. Trigger occurs (e.g., Verstappen pits for Inters on Lap 40 at Spa).
  2. Orchestrator queries Qdrant for "Spa wet weather strategy" or "Verstappen intermediate pace at Spa".
  3. Top-K results are injected into the system prompt.

## 4. Prompt Engineering & Grounding

Prompts are strictly templated. The LLM is explicitly instructed to cite the model version and confidence score provided in the structured payload.

**System Prompt Example Excerpt:**
> You are the PitWall AI Race Engineer. You are analyzing the attached structured prediction from the 'tyre-degradation-v1.2' model.
> Do not invent lap times. Do not invent pit strategies. Only explain the data provided.
> The model predicts Lando Norris will pit between lap 28 and 30 with 82% confidence. Explain why this makes sense based on the attached track temperature and his current medium tyre stint.

## 5. Model Versioning & Evaluation

- **Prediction Models**: Evaluated using standard ML metrics (MAE, RMSE, Brier Score) across historical replays. A model cannot be promoted to production without passing the validation gate.
- **LLM Evaluation**: Evaluated using LLM-as-a-Judge against a golden dataset of race scenarios to test for hallucination (e.g., claiming a driver is on hard tyres when the structured data says mediums).
