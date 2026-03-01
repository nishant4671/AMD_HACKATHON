from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Risk(Base):
    __tablename__ = "risks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    college_id = Column(String(64), index=True)
    student_id = Column(String(64), index=True)
    subject = Column(String(64), index=True)
    quiz1 = Column(Float)
    quiz2 = Column(Float)
    quiz3 = Column(Float)
    attendance = Column(Float)
    risk_level = Column(String(16))  # HIGH, MEDIUM, LOW
    xp_score = Column(Integer, default=0)
    reason = Column(String(256), nullable=True)
    teacher_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Intervention(Base):
    __tablename__ = "interventions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    college_id = Column(String(64))
    student_id = Column(String(64))
    teacher_id = Column(String(64))
    action = Column(String(64))
    success = Column(Boolean, default=False)
    xp_earned = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
