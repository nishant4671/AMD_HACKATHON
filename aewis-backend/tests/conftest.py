import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Project root
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

os.environ["DATABASE_URL"] = "sqlite:///./test_aewis.db"

from app.main import app
from app.db.session import init_db

init_db()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def demo_csv_path():
    p = root / "demo_data.csv"
    if not p.exists():
        from utils.data_generator import write_demo_csv
        write_demo_csv(p, 512)
    return p
