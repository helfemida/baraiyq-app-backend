from fastapi.testclient import TestClient
from src.app import app
from unittest.mock import MagicMock

client = TestClient(app)

def test_get_orders_success(mocker):
    mock_get_orders_managers = mocker.patch('app.router.get_orders_managers', return_value=[{"id": 1, "status": "completed"}])
    response = client.get("/orders/1/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "status": "completed"}]
    mock_get_orders_managers.assert_called_once_with(1, mocker.ANY)

def test_get_orders_not_found(mocker):
    mocker.patch('app.router.get_orders_managers', return_value=[])
    response = client.get("/orders/999/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_orders_invalid_id():
    response = client.get("/orders/invalid/")
    assert response.status_code == 422

def test_get_orders_db_error(mocker):
    mocker.patch('app.router.get_orders_managers', side_effect=Exception("Database error"))
    response = client.get("/orders/1/")
    assert response.status_code == 500

def test_get_orders_large_data(mocker):
    large_data = [{"id": i, "status": "completed"} for i in range(1000)]
    mocker.patch('app.router.get_orders_managers', return_value=large_data)
    response = client.get("/orders/1/")
    assert response.status_code == 200
    assert len(response.json()) == 1000
