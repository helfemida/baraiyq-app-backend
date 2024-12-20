from fastapi.testclient import TestClient
from src.app import app
from unittest.mock import patch
import pytest

client = TestClient(app)

@pytest.fixture
def mock_check_office_availability():
    with patch('src.orders.check_office_availability') as mock_check:
        yield mock_check

def test_successful_booking_of_multiple_premises():
    with patch('src.orders.check_office_availability', return_value=[1, 2]):
        order_data = {
            "office_id": 1,
            "client_id": 1,
            "office_name": "Office 1",
            "office_desc": "A nice office",
            "address": "123 Main St",
            "max_capacity": 10,
            "duration": "2024-12-10T09:00-2024-12-10T17:00",
            "status": "Booked",
            "total_sum": 500.0,
            "services": [{"service_name": "Food"}, {"service_name": "Entertainment"}]
        }
        response = client.post("/order/1/", json=order_data)

        assert response.status_code == 200
        assert "order_id" in response.json()

def test_exceeded_booking_limit():
    with patch('src.orders.check_office_availability', return_value=[1, 2, 3]):
        order_data = {
            "office_id": 1,
            "client_id": 1,
            "office_name": "Office 1",
            "office_desc": "A nice office",
            "address": "123 Main St",
            "max_capacity": 10,
            "duration": "2024-12-10T09:00-2024-12-10T17:00",
            "status": "Booked",
            "total_sum": 500.0,
            "services": [{"service_name": "Food"}, {"service_name": "Entertainment"}]
        }
        response = client.post("/order/1/", json=order_data)

        assert response.status_code == 406
        assert response.json()["detail"] == "The office is not available for the requested duration. Maximum of 3 overlapping orders allowed."


def test_retrieve_client_orders():
    mock_orders = [
        {
            "id": 1,
            "office_name": "Office 1",
            "status": "Booked",
            "services": [{"service_name": "Food"}, {"service_name": "Entertainment"}]
        }
    ]

    with patch('src.orders.get_orders_by_client_id_service', return_value=mock_orders):
        response = client.get("/orders/1/")

    assert response.status_code == 200
    orders = response.json()
    assert len(orders) == 1
    assert orders[0]["office_name"] == "Office 1"
    assert "Food" in orders[0]["services"][0]["service_name"]


def test_no_orders_for_client():
    with patch('app.orders.get_orders_by_client_id_service', return_value=[]):
        response = client.get("/orders/1/")

    assert response.status_code == 200
    assert response.json() == []


def test_successful_review_submission():
    feedback_data = {
        "client_id": 1,
        "office_id": 1,
        "title": "Great Experience!",
        "description": "The office was amazing and well-equipped.",
        "rating": 5
    }

    with patch('app.offices.add_feedback') as mock_add_feedback:
        mock_add_feedback.return_value = feedback_data
        response = client.post("/offices/feedbacks/post/", json=feedback_data)

    assert response.status_code == 200
    assert response.json()["rating"] == 5
    mock_add_feedback.assert_called_once_with(mock.ANY, feedback_data)


def test_review_submission_missing_rating():
    feedback_data = {
        "client_id": 1,
        "office_id": 1,
        "title": "Not bad",
        "description": "The office was okay.",
        "rating": None
    }

    response = client.post("/offices/feedbacks/post/", json=feedback_data)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_select_multiple_services():
    order_data = {
        "office_id": 1,
        "client_id": 1,
        "office_name": "Office 1",
        "office_desc": "A nice office",
        "address": "123 Main St",
        "max_capacity": 10,
        "duration": "2024-12-10T09:00-2024-12-10T17:00",
        "status": "Booked",
        "total_sum": 500.0,
        "services": [{"service_name": "Food"}, {"service_name": "Entertainment"}, {"service_name": "AV Equipment"}]
    }

    response = client.post("/order/1/", json=order_data)

    assert response.status_code == 200
    assert len(response.json()["services"]) == 3
    assert "AV Equipment" in response.json()["services"][2]["service_name"]


def test_select_no_service():
    order_data = {
        "office_id": 1,
        "client_id": 1,
        "office_name": "Office 1",
        "office_desc": "A nice office",
        "address": "123 Main St",
        "max_capacity": 10,
        "duration": "2024-12-10T09:00-2024-12-10T17:00",
        "status": "Booked",
        "total_sum": 500.0,
        "services": []
    }

    response = client.post("/order/1/", json=order_data)

    assert response.status_code == 200
    assert response.json()["services"] == []


def test_successful_feedback_rating():
    feedback_data = {
        "client_id": 1,
        "office_id": 1,
        "title": "Great Experience!",
        "description": "The office was amazing and well-equipped.",
        "rating": 5
    }

    with patch('app.offices.add_feedback') as mock_add_feedback:
        mock_add_feedback.return_value = feedback_data
        response = client.post("/offices/feedbacks/post/", json=feedback_data)

    assert response.status_code == 200
    assert response.json()["rating"] == 5
    mock_add_feedback.assert_called_once_with(mock.ANY, feedback_data)


def test_feedback_with_missing_rating():
    feedback_data = {
        "client_id": 1,
        "office_id": 1,
        "title": "Good service",
        "description": "Overall good, but could improve cleanliness.",
        "rating": None
    }

    response = client.post("/offices/feedbacks/post/", json=feedback_data)

    assert response.status_code == 422
    assert "detail" in response.json()
