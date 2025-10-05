import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pathlib
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import init_db, engine

DB_FILE = pathlib.Path("rideplanner.sqlite3")

@pytest.fixture(autouse=True)
def _fresh_db():
    try:
        engine.dispose()
    except Exception:
        pass

    if DB_FILE.exists():
        DB_FILE.unlink()
    init_db()

    yield

    try:
        engine.dispose()
    except Exception:
        pass
    if DB_FILE.exists():
        DB_FILE.unlink()
 
@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c
