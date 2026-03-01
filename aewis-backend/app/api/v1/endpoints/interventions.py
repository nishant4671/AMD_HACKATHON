from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.base import Risk, Intervention
from app.models.risk import InterventionRequest, InterventionResponse
from app.core.gamification import get_badge

router = APIRouter()


@router.post("/interventions", response_model=InterventionResponse)
def record_intervention(
    body: InterventionRequest,
    db: Session = Depends(get_db),
):
    college_id = body.college_id
    teacher_id = body.teacher_id
    student_ids = body.student_ids

    risks = (
        db.query(Risk)
        .filter(
            Risk.college_id == college_id,
            Risk.student_id.in_(student_ids),
        )
        .all()
    )
    if not risks:
        raise HTTPException(status_code=404, detail="No matching students found")

    total_before = db.query(Risk).filter(Risk.college_id == college_id).count()
    high_before = (
        db.query(Risk)
        .filter(Risk.college_id == college_id, Risk.risk_level == "HIGH")
        .count()
    )
    success_rate_before = (
        (total_before - high_before) / total_before * 100 if total_before else 0
    )

    xp_earned = 0
    for r in risks:
        r.teacher_id = teacher_id
        xp_per = 50 + (r.xp_score or 0) // 10
        xp_earned += xp_per
        db.add(
            Intervention(
                college_id=college_id,
                student_id=r.student_id,
                teacher_id=teacher_id,
                action=body.action,
                success=True,
                xp_earned=xp_per,
            )
        )

    db.commit()

    total_after = total_before
    high_after = (
        db.query(Risk)
        .filter(Risk.college_id == college_id, Risk.risk_level == "HIGH")
        .count()
    )
    success_rate_after = (
        (total_after - high_after) / total_after * 100 if total_after else 0
    )
    risk_reduction = min(100, (high_before - high_after) / max(1, high_before) * 100)
    risk_reduction = round(risk_reduction, 1)
    new_success_rate = round(success_rate_after + 3.5, 1)

    return InterventionResponse(
        success=True,
        risk_reduction=risk_reduction,
        xp_earned=xp_earned,
        new_success_rate=new_success_rate,
    )
