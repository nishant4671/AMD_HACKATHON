# Backend Architecture Guide

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://localhost:8000/docs**

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/upload-csv | Upload CSV → Risk analysis, store in DB |
| GET  | /api/v1/risk-stats/{college_id} | College analytics, KPIs, charts, heatmap |
| POST | /api/v1/interventions | Record teacher interventions, XP, risk reduction |
| GET  | /api/v1/teacher/{teacher_id}/students | Teacher-specific risk list for dashboard |

## Database Schema

- **risks**: college_id, student_id, subject, quiz1–3, attendance, risk_level, xp_score, reason, teacher_id, created_at  
- **interventions**: college_id, student_id, teacher_id, action, success, xp_earned, created_at  

See `app/db/base.py` for ORM models.

## Frontend Integration

```python
import requests

BACKEND_URL = "http://localhost:8000"

# 1. Upload CSV
with open("demo_data.csv", "rb") as f:
    r = requests.post(f"{BACKEND_URL}/api/v1/upload-csv", files={"file": f}, data={"college_id": "demo"})
risk_data = r.json()

# 2. Get heatmap matrix
r = requests.get(f"{BACKEND_URL}/api/v1/risk-stats/demo_001")
heatmap = r.json()["heatmap_matrix"]

# 3. Record intervention
requests.post(f"{BACKEND_URL}/api/v1/interventions", json={
    "college_id": "demo_001",
    "teacher_id": "T001_Sharma",
    "student_ids": ["S101", "S105"],
    "action": "intervene",
})
```

## Scaling Notes

- **Hackathon**: 1 college, SQLite  
- **Month 2**: 10 colleges → Postgres + Redis  
- **Month 6**: 100 colleges → Kubernetes + Celery  
- **Year 1**: ML predictions → Vector DB  

SQLite → Postgres: set `DATABASE_URL` to Postgres and run migrations (e.g. Alembic). No code changes required for session layer.
