import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_all_offices():
    response = client.get("/clients/offices")
    assert response.status_code == 200
    assert "name" in response.json()

def test_get_office_details():
    response = client.get("/clients/offices/1")
    assert response.status_code == 200
    assert "name" in response.json()

def test_get_nonexistent_office():
    response = client.get("/clients/offices/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Office not found"}

