import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("HUB_OPENCLAW_TOKEN", "test-token")

from app.main import app  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}
