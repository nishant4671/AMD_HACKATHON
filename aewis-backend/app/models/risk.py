from pydantic import BaseModel
from typing import List, Optional, Any


class RiskModel(BaseModel):
    risk_level: str  # HIGH | MEDIUM | LOW
    reason: str
    xp_score: int
    health_score: int


class UploadSummary(BaseModel):
    total_students: int
    high_risk: int
    medium_risk: int
    low_risk: int
    crisis_subjects: List[str]


class TopRisk(BaseModel):
    student_id: str
    subject: str
    risk: str
    reason: str


class UploadResponse(BaseModel):
    success: bool
    college_id: str
    summary: UploadSummary
    heatmap_matrix: List[List[Any]]
    top_risks: List[TopRisk]


class InterventionRequest(BaseModel):
    college_id: str
    teacher_id: str
    student_ids: List[str]
    action: str = "intervene"


class InterventionResponse(BaseModel):
    success: bool
    risk_reduction: float
    xp_earned: int
    new_success_rate: float


class RiskStatsKPIs(BaseModel):
    health_score: float
    risk_trend: float
    success_rate: float


class RiskStatsCharts(BaseModel):
    risk_distribution: List[Any]
    subject_risks: dict
    decline_trends: List[Any]


class RiskStatsResponse(BaseModel):
    college_id: str
    kpis: RiskStatsKPIs
    charts: RiskStatsCharts
    heatmap_matrix: Optional[List[List[Any]]] = None


class TeacherStudentRisk(BaseModel):
    student_id: str
    subject: str
    risk_level: str
    reason: str
    xp_score: int
