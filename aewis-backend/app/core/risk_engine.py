from enum import Enum
from app.models.risk import RiskModel


class RiskLevelEnum(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


def compute_risk(row: dict) -> RiskModel:
    quiz1 = float(row.get("quiz1", 0))
    quiz2 = float(row.get("quiz2", 0))
    quiz3 = float(row.get("quiz3", 0))
    attendance = float(row.get("attendance", 0))

    avg_score = (quiz1 + quiz2 + quiz3) / 3 if (quiz1 or quiz2 or quiz3) else 0
    decline_pct = (
        (quiz1 - quiz3) / quiz1 * 100
        if quiz1 and quiz1 > 0
        else 0
    )

    reasons = []
    if attendance < 75:
        reasons.append("Attendance")
    if decline_pct > 15:
        reasons.append("Decline")
    if avg_score < 40:
        reasons.append("Average")

    if len(reasons) >= 2:
        risk_level = RiskLevelEnum.HIGH.value
    elif len(reasons) == 1:
        risk_level = RiskLevelEnum.MEDIUM.value
    else:
        risk_level = RiskLevelEnum.LOW.value

    xp_score = int(avg_score * 10)
    health_score = min(100, max(0, int(avg_score)))

    return RiskModel(
        risk_level=risk_level,
        reason="+".join(reasons) if reasons else "OK",
        xp_score=xp_score,
        health_score=health_score,
    )
