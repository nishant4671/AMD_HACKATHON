from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.base import Risk
from app.models.risk import RiskStatsResponse, RiskStatsKPIs, RiskStatsCharts

router = APIRouter()


@router.get("/risk-stats/{college_id}", response_model=RiskStatsResponse)
def get_risk_stats(college_id: str, db: Session = Depends(get_db)):
    rows = db.query(Risk).filter(Risk.college_id == college_id).all()
    if not rows:
        raise HTTPException(status_code=404, detail="College not found or no data")

    total = len(rows)
    high = sum(1 for r in rows if r.risk_level == "HIGH")
    medium = sum(1 for r in rows if r.risk_level == "MEDIUM")
    low = sum(1 for r in rows if r.risk_level == "LOW")

    avg_health = sum((r.quiz1 + r.quiz2 + r.quiz3) / 3 for r in rows) / total if total else 0
    health_score = round(avg_health, 1)
    success_rate = round((low + medium * 0.5) / total * 100, 1) if total else 0

    risk_distribution = [
        {"level": "HIGH", "count": high},
        {"level": "MEDIUM", "count": medium},
        {"level": "LOW", "count": low},
    ]

    subject_risks = defaultdict(float)
    subject_counts = defaultdict(int)
    for r in rows:
        subject_risks[r.subject] += 1 if r.risk_level == "HIGH" else 0
        subject_counts[r.subject] += 1
    subject_risks_pct = {
        s: round(subject_risks[s] / subject_counts[s] * 100, 1)
        for s in subject_counts
    }

    decline_trends = []
    by_student_subject = defaultdict(list)
    for r in rows:
        key = (r.student_id, r.subject)
        by_student_subject[key].append((r.quiz1, r.quiz2, r.quiz3))
    for key, quizzes in list(by_student_subject.items())[:50]:
        if quizzes:
            q1, q2, q3 = quizzes[0]
            decline = ((q1 - q3) / q1 * 100) if q1 and q1 > 0 else 0
            decline_trends.append({"student_id": key[0], "subject": key[1], "decline_pct": round(decline, 1)})

    heatmap_matrix = [
        [r.student_id, r.subject, r.risk_level, r.xp_score, (r.quiz1 + r.quiz2 + r.quiz3) / 3]
        for r in rows[:200]
    ]

    kpis = RiskStatsKPIs(
        health_score=health_score,
        risk_trend=-12.5,
        success_rate=success_rate,
    )
    charts = RiskStatsCharts(
        risk_distribution=risk_distribution,
        subject_risks=subject_risks_pct,
        decline_trends=decline_trends,
    )

    return RiskStatsResponse(
        college_id=college_id,
        kpis=kpis,
        charts=charts,
        heatmap_matrix=heatmap_matrix,
    )
