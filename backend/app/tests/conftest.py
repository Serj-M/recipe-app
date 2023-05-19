import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@pytest.fixture(scope='module')
def client():
    client = TestClient(app)
    yield client
