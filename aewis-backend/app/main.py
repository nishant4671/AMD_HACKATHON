from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.router import api_router
from app.db.session import init_db

app = FastAPI(
    title="AEWIS API",
    description="Academic Early Warning & Intervention System - Production Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

_origins = [o for o in settings.CORS_ORIGINS if "*" not in o]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_origin_regex=r"https://.*\.streamlit\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health():
    return {"status": "ok", "service": "aewis-backend"}
