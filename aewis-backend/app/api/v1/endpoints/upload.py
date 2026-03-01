import io
import pandas as pd
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict

from app.api.deps import get_db
from app.db.base import Risk
from app.core.risk_engine import compute_risk
from app.models.risk import UploadResponse, UploadSummary, TopRisk

router = APIRouter()


@router.post("/upload-csv", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    college_id: str = Form("demo"),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV file required")

    content = await file.read()
    try:
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {str(e)}")

    required = ["student_id", "subject", "quiz1", "quiz2", "quiz3", "attendance"]
    for col in required:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing column: {col}")

    # Normalize college_id
    cid = f"{college_id}_001" if college_id == "demo" else college_id

    # Delete existing risks for this college to avoid duplicates
    db.query(Risk).filter(Risk.college_id == cid).delete()
    db.commit()

    high, medium, low = 0, 0, 0
    subject_high_count = defaultdict(int)
    subject_total = defaultdict(int)
    records = []
    top_risks = []
    matrix_rows = []

    for _, row in df.iterrows():
        r = row.to_dict()
        computed = compute_risk(r)
        if computed.risk_level == "HIGH":
            high += 1
        elif computed.risk_level == "MEDIUM":
            medium += 1
        else:
            low += 1

        subject_total[r["subject"]] += 1
        if computed.risk_level == "HIGH":
            subject_high_count[r["subject"]] += 1

        rec = Risk(
            college_id=cid,
            student_id=str(r["student_id"]),
            subject=str(r["subject"]),
            quiz1=float(r["quiz1"]),
            quiz2=float(r["quiz2"]),
            quiz3=float(r["quiz3"]),
            attendance=float(r["attendance"]),
            risk_level=computed.risk_level,
            xp_score=computed.xp_score,
            reason=computed.reason,
        )
        records.append(rec)
        if computed.risk_level == "HIGH" and len(top_risks) < 20:
            top_risks.append(
                TopRisk(
                    student_id=str(r["student_id"]),
                    subject=str(r["subject"]),
                    risk=computed.risk_level,
                    reason=computed.reason,
                )
            )
        matrix_rows.append(
            [
                r["student_id"],
                r["subject"],
                computed.risk_level,
                computed.xp_score,
                computed.health_score,
            ]
        )

    db.add_all(records)
    db.commit()

    # Crisis subjects: >30% high risk
    crisis_subjects = [
        s
        for s in subject_total
        if subject_total[s] > 0
        and subject_high_count[s] / subject_total[s] > 0.30
    ]
    crisis_subjects = sorted(crisis_subjects)

    heatmap_matrix = matrix_rows

    summary = UploadSummary(
        total_students=len(records),
        high_risk=high,
        medium_risk=medium,
        low_risk=low,
        crisis_subjects=crisis_subjects,
    )

    return UploadResponse(
        success=True,
        college_id=cid,
        summary=summary,
        heatmap_matrix=heatmap_matrix,
        top_risks=top_risks,
    )
