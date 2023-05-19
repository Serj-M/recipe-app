import pytest
from fastapi.testclient import TestClient

from ..app import app


@pytest.fixture(scope='module')
def client():
    client = TestClient(app)
    yield client
