import sys
from pathlib import Path
import pytest

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from app.core.risk_engine import compute_risk, RiskLevelEnum


def test_compute_risk_high_attendance_decline():
    row = {"quiz1": 80, "quiz2": 70, "quiz3": 50, "attendance": 70}
    r = compute_risk(row)
    assert r.risk_level in (RiskLevelEnum.HIGH.value, RiskLevelEnum.MEDIUM.value)
    assert "Decline" in r.reason or "Attendance" in r.reason


def test_compute_risk_low_avg():
    row = {"quiz1": 30, "quiz2": 35, "quiz3": 32, "attendance": 90}
    r = compute_risk(row)
    assert r.risk_level in (RiskLevelEnum.HIGH.value, RiskLevelEnum.MEDIUM.value)
    assert r.xp_score <= 400


def test_compute_risk_low():
    row = {"quiz1": 75, "quiz2": 78, "quiz3": 76, "attendance": 88}
    r = compute_risk(row)
    assert r.risk_level == RiskLevelEnum.LOW.value
    assert r.reason == "OK" or r.reason == ""


def test_physics_crisis_cluster():
    from utils.data_generator import generate_demo_data
    import pandas as pd
    data = generate_demo_data(512)
    df = pd.DataFrame(data)
    from app.core.risk_engine import compute_risk
    risks = []
    for _, row in df.iterrows():
        r = compute_risk(row.to_dict())
        risks.append(r.risk_level)
    df["risk_level"] = risks
    physics = df[df["subject"] == "Physics"]["risk_level"]
    if len(physics) > 0:
        high_pct = (physics == "HIGH").sum() / len(physics)
        assert high_pct > 0.20, "Physics should show elevated high-risk share"
