import sys
from pathlib import Path
import pytest

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_docs_available(client):
    r = client.get("/docs")
    assert r.status_code == 200


def test_upload_csv(client, demo_csv_path):
    with open(demo_csv_path, "rb") as f:
        r = client.post(
            "/api/v1/upload-csv",
            files={"file": ("demo_data.csv", f, "text/csv")},
            data={"college_id": "demo"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    assert "demo_001" in body["college_id"]
    assert body["summary"]["total_students"] > 0
    assert "heatmap_matrix" in body
    assert "top_risks" in body


def test_risk_stats_after_upload(client, demo_csv_path):
    with open(demo_csv_path, "rb") as f:
        client.post(
            "/api/v1/upload-csv",
            files={"file": ("demo_data.csv", f, "text/csv")},
            data={"college_id": "demo"},
        )
    r = client.get("/api/v1/risk-stats/demo_001")
    assert r.status_code == 200
    body = r.json()
    assert body["college_id"] == "demo_001"
    assert "kpis" in body
    assert "charts" in body
    assert "heatmap_matrix" in body


def test_intervention_success(client, demo_csv_path):
    with open(demo_csv_path, "rb") as f:
        client.post(
            "/api/v1/upload-csv",
            files={"file": ("demo_data.csv", f, "text/csv")},
            data={"college_id": "demo"},
        )
    r = client.post(
        "/api/v1/interventions",
        json={
            "college_id": "demo_001",
            "teacher_id": "T001_Sharma",
            "student_ids": ["S101", "S105"],
            "action": "intervene",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    assert "risk_reduction" in body
    assert "xp_earned" in body
    assert body["xp_earned"] >= 0


def test_teacher_students(client, demo_csv_path):
    with open(demo_csv_path, "rb") as f:
        client.post(
            "/api/v1/upload-csv",
            files={"file": ("demo_data.csv", f, "text/csv")},
            data={"college_id": "demo"},
        )
    r = client.get("/api/v1/teacher/T001_Sharma/students")
    assert r.status_code == 200
    body = r.json()
    assert "students" in body
    assert body["teacher_id"] == "T001_Sharma"
