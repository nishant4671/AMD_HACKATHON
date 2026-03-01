"""
Seed demo data into SQLite for development.
Uses utils.data_generator and risk engine to populate risks table.
"""
import sys
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.db.session import SessionLocal, init_db
from app.db.base import Risk
from app.core.risk_engine import compute_risk


def seed_demo(college_id: str = "demo_001", num_rows: int = 512):
    from utils.data_generator import generate_demo_data

    init_db()
    db = SessionLocal()
    try:
        db.query(Risk).filter(Risk.college_id == college_id).delete()
        db.commit()
        rows = generate_demo_data(num_rows)
        for r in rows:
            computed = compute_risk(r)
            rec = Risk(
                college_id=college_id,
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
            db.add(rec)
        db.commit()
        print(f"Seeded {len(rows)} rows for college_id={college_id}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo()
