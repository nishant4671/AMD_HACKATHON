# SQLAlchemy ORM models are defined in app/db/base.py
# This module re-exports for convenience
from app.db.base import Risk, Intervention, Base

__all__ = ["Risk", "Intervention", "Base"]
