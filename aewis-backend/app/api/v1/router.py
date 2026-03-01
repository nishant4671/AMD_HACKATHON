from fastapi import APIRouter
from app.api.v1.endpoints import upload, analytics, interventions, teacher

api_router = APIRouter()

api_router.include_router(upload.router, prefix="", tags=["upload"])
api_router.include_router(analytics.router, prefix="", tags=["analytics"])
api_router.include_router(interventions.router, prefix="", tags=["interventions"])
api_router.include_router(teacher.router, prefix="", tags=["teacher"])
