import pytest
from fastapi.testclient import TestClient

from app import create_app


@pytest.fixture
def app():
    app_instance = create_app()
    return TestClient(app_instance)
