from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.base import Risk
from app.models.risk import TeacherStudentRisk

router = APIRouter()


@router.get("/teacher/{teacher_id}/students")
def get_teacher_students(
    teacher_id: str,
    college_id: str = Query("demo_001", description="College ID"),
    db: Session = Depends(get_db),
):
    """Teacher-specific risk list for dashboard."""
    all_risks = (
        db.query(Risk)
        .filter(Risk.college_id == college_id)
        .order_by(Risk.risk_level.desc())
        .limit(100)
        .all()
    )
    result = [
        TeacherStudentRisk(
            student_id=r.student_id,
            subject=r.subject,
            risk_level=r.risk_level,
            reason=r.reason or "",
            xp_score=r.xp_score or 0,
        )
        for r in all_risks
    ]
    return {"teacher_id": teacher_id, "college_id": college_id, "students": result}
