<div align="center">

# 🧠 Adaptive Learning Engine
### A transparent, API-driven practice and revision system

**Python · FastAPI · spaced repetition · skill mastery · unit & API tests**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![CI](https://github.com/ibrar1921/adaptive-learning-engine/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ibrar1921/adaptive-learning-engine/actions/workflows/python-tests.yml)

[API endpoints](#api-reference) · [Scheduling algorithm](docs/scheduling.md) · [Tests](test_engine.py)

</div>

---

## 🎯 What does it do?

Learning systems often treat everyone the same. **Adaptive Learning Engine** is a small, explainable backend that changes quiz order based on skill progress and review due dates, then returns helpful answer explanations.

Inspired by Ibrar Pervaiz's academic **Intelligent Tutoring System** interests, this repo demonstrates software architecture for educational technology — **not** an unverified deep-learning model.

## ✨ Working functionality

- **12 original multiple-choice questions** across Python, SQL and machine learning.
- **RESTful session API** for creating sessions, fetching questions, submitting answers and reviewing progress.
- **Rule-based adaptation:** prefer unattempted material, weaker skills and items due for review.
- **Simple spaced review:** correct answers increase the next-review interval; mistakes schedule faster review.
- **Interpretable mastery estimate:** smoothed success fraction by skill, not a scientifically calibrated learning score.
- Data validation, consistent HTTP errors, shared-state synchronization, pure engine unit tests and API checks.

## ⚡ Getting started

Requires Python 3.11+.

```bash
git clone https://github.com/ibrar1921/adaptive-learning-engine.git
cd adaptive-learning-engine
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -v
uvicorn api:app --reload
```

Open **http://127.0.0.1:8000/docs** for Swagger UI.

## 🌐 API reference

| Method | Route | Purpose |
|:---|:---|:---|
| `GET` | `/health` | Readiness check |
| `POST` | `/sessions` | Create a new in-memory learning session |
| `GET` | `/sessions/{sid}/next` | Fetch next question (without revealing the solution) |
| `POST` | `/sessions/{sid}/answer` | Submit selected answer |
| `GET` | `/sessions/{sid}/progress` | Review mastery estimates and attempts |

### Example workflow

```bash
# 1. Create a session and copy the returned session_id
curl -X POST http://127.0.0.1:8000/sessions

# 2. Replace SESSION_ID with the returned UUID
curl http://127.0.0.1:8000/sessions/SESSION_ID/next

# 3. Use the question_id returned above, and a zero-based choice index
curl -X POST http://127.0.0.1:8000/sessions/SESSION_ID/answer \
  -H "Content-Type: application/json" \
  -d '{"question_id":"ML1","choice":1}'

# 4. Inspect progress
curl http://127.0.0.1:8000/sessions/SESSION_ID/progress
```

Use the **actual returned question_id** in step 3; `ML1` above is only an example.

## 🧩 Architecture

```text
Client / Swagger UI
        │
        ▼
FastAPI endpoints ───> Session state (memory)
        │                       │
        ▼                       ▼
Question selection <── Mastery & review schedule
        │
        ▼
Answer feedback + next review turn
```

Project files:

```text
├── api.py                  # HTTP endpoints and validation
├── engine.py               # Questions and review scheduling
├── test_engine.py          # Deterministic rule tests
├── test_api.py             # HTTP endpoint tests
├── docs/scheduling.md      # Explainable algorithm
└── .github/workflows/python-tests.yml
```

## 🔬 Research potential and limitations

The system implements **explicit rules**, not machine learning, deep learning, or an evidence-based knowledge tracing model. Sessions are **in-memory**, lost after restart and not authenticated; therefore this is a local prototype, not a deployment-ready student platform. Review timing uses interaction turns rather than wall-clock dates.

Research extensions:
- [ ] Compare heuristic scheduling with Bayesian Knowledge Tracing / Deep Knowledge Tracing
- [ ] Add PostgreSQL-backed users, sessions and authenticated roles
- [ ] Experiment with difficulty and item-response models
- [ ] Define ethical evaluation, privacy policies and student-outcome metrics
- [ ] Build an accessible Angular or React student interface

## 👤 Author

**Ibrar Pervaiz** · MSc Computer Science · Software Engineer, K.M.S Business Services Ltd.

[GitHub](https://github.com/ibrar1921) · [LinkedIn](https://www.linkedin.com/in/ibrar-pervaiz-0b1a2a158/)
