from fastapi.testclient import TestClient
from src.app import app
from unittest.mock import MagicMock

client = TestClient(app)
def test_update_order_status_success(mocker):
    mock_update_service = mocker.patch('app.router.update_order_status_service')
    response = client.put("/orders/1/status/", json={"order_id": 1, "status": "completed"})
    assert response.status_code == 200
    assert response.json() == {"message": "Order status updated successfully"}
    mock_update_service.assert_called_once_with(mocker.ANY, {"order_id": 1, "status": "completed"})

def test_update_order_status_invalid_request():
    response = client.put("/orders/1/status/", json={})
    assert response.status_code == 422

def test_update_order_status_not_found(mocker):
    mocker.patch('app.router.update_order_status_service', side_effect=ValueError("Order not found"))
    response = client.put("/orders/1/status/", json={"order_id": 999, "status": "completed"})
    assert response.status_code == 400

def test_update_order_status_db_error(mocker):
    mocker.patch('app.router.update_order_status_service', side_effect=Exception("Database error"))
    response = client.put("/orders/1/status/", json={"order_id": 1, "status": "completed"})
    assert response.status_code == 500

def test_update_order_status_unauthorized(mocker):
    response = client.put("/orders/1/status/", json={"order_id": 1, "status": "completed"}, headers={"Authorization": "InvalidToken"})
    assert response.status_code == 401
