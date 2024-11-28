from src.app import app
from unittest.mock import MagicMock

def test_create_schedule_success(mocker):
    mock_create_service = mocker.patch('app.router.create_schedule_service', return_value=MagicMock(id=1))
    response = client.post("/create-schedule/1/", json={"start_time": "10:00", "end_time": "18:00"})
    assert response.status_code == 200
    assert response.json() == {"message": "Schedule 1 created successfully!"}
    mock_create_service.assert_called_once_with(1, mocker.ANY, {"start_time": "10:00", "end_time": "18:00"})

def test_create_schedule_invalid_request():
    response = client.post("/create-schedule/1/", json={})
    assert response.status_code == 422

def test_create_schedule_office_not_found(mocker):
    mocker.patch('app.router.create_schedule_service', side_effect=ValueError("Office not found"))
    response = client.post("/create-schedule/999/", json={"start_time": "10:00", "end_time": "18:00"})
    assert response.status_code == 400

def test_create_schedule_db_error(mocker):
    mocker.patch('app.router.create_schedule_service', side_effect=Exception("Database error"))
    response = client.post("/create-schedule/1/", json={"start_time": "10:00", "end_time": "18:00"})
    assert response.status_code == 500

def test_create_schedule_conflict(mocker):
    mocker.patch('app.router.create_schedule_service', side_effect=ValueError("Schedule conflict"))
    response = client.post("/create-schedule/1/", json={"start_time": "10:00", "end_time": "18:00"})
    assert response.status_code == 409
