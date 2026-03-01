# AEWIS Backend – Academic Early Warning & Intervention System

Production-ready FastAPI backend for the AEWIS Academic Early Warning System.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000/docs** for Swagger UI.

## Generate demo data (512 rows)

```bash
python -c "from utils.data_generator import write_demo_csv; write_demo_csv('demo_data.csv', 512)"
```

Optional: seed DB with demo data:

```bash
python -m app.db.seed
```

## Test API

```bash
# Upload CSV
curl -X POST "http://localhost:8000/api/v1/upload-csv" -F "file=@demo_data.csv" -F "college_id=demo"

# Risk stats
curl "http://localhost:8000/api/v1/risk-stats/demo_001"

# Record intervention
curl -X POST "http://localhost:8000/api/v1/interventions" \
  -H "Content-Type: application/json" \
  -d '{"college_id":"demo_001","teacher_id":"T001_Sharma","student_ids":["S101","S105"],"action":"intervene"}'
```

## Run tests

```bash
pytest tests/ -v
```

## Docker

```bash
docker build -t aewis-backend .
docker run -p 8000:8000 aewis-backend
```

## Environment

| Variable         | Default                |
|------------------|------------------------|
| `DATABASE_URL`   | `sqlite:///./aewis.db` |
| `DEBUG`          | `True`                 |
| `API_V1_STR`     | `/api/v1`              |

See **BACKEND_ARCHITECTURE_GUIDE.md** for full architecture and scaling notes.
