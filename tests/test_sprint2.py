from http.client import HTTPException
from unittest import mock

from fastapi.testclient import TestClient
from src.app import app
from unittest.mock import patch
import pytest

client = TestClient(app)

@pytest.fixture
def mock_get_offices_info():
    with patch('src.repositories.offices.get_all_offices') as mock_get:
        yield mock_get

def test_browse_premises(mock_get_offices_info):
    response = client.get("/clients/offices/")

    assert response.status_code == 200

    assert "offices" in response.json()
    assert len(response.json()["offices"]) == 14

@pytest.fixture
def mock_get_single_office():
    with patch('src.repositories.offices.get_office_dto_by_id') as mock_get:
        yield mock_get

def test_view_office_information(mock_get_single_office):
    mock_get_single_office.return_value = {
        "id": 4,
        "name": "Tech Park",
        "description": "Innovative Space for tech startups",
        "address": "18 Auezov Avenue, Almaty",
        "rating": 4.3,
        "capacity": 150,
        "lat": 42.315407,
        "lng": 69.589538,
    }

    response = client.get("/clients/offices/4/")

    assert response.status_code == 200

    office = response.json()
    assert office["name"] == "Tech Park"
    assert office["address"] == "18 Auezov Avenue, Almaty"
    assert "schedule" in office
    assert "feedbacks" in office


def test_view_office_not_found(mock_get_single_office):
    response = client.get("/clients/offices/999/")

    assert response.status_code == 404

    assert response.json()["detail"] == "Office not found"
