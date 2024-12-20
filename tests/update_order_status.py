from unittest.mock import patch, MagicMock

from tests.client_auth_tests import client


def test_create_schedule_success():
    office_id = 1
    schedule_data = {
        "day": "Monday",
        "start_time": "10:00",
        "end_time": "18:00"
    }

    # Mocking database calls
    with patch('app.schedule.create_schedule', return_value=MagicMock(id=1)):
        response = client.post(f"/create-schedule/{office_id}/", json=schedule_data)

        assert response.status_code == 200
        assert response.json()["message"] == "Schedule 1 created successfully!"

def test_create_schedule_office_not_found():
    office_id = 999
    schedule_data = {
        "day": "Monday",
        "start_time": "10:00",
        "end_time": "18:00"
    }

    # Mocking database calls
    with patch('app.schedule.get_office_by_id', return_value=None):
        response = client.post(f"/create-schedule/{office_id}/", json=schedule_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Office not found"

def test_create_office_success():
    office_data = {
        "name": "Event Hall",
        "description": "A spacious event hall for conferences",
        "address": "123 Event St",
        "capacity": 200,
    }

    # Mocking database calls
    with patch('app.offices.create_office_manager', return_value=MagicMock(id=1)):
        response = client.post("/create-office/", json=office_data)

        assert response.status_code == 200
        assert response.json()["message"] == "Office 1 created successfully!"

def test_update_office_not_found():
    office_data = {
        "id": 999,
        "name": "Updated Event Hall",
        "description": "An updated description",
        "address": "123 New Event St",
        "capacity": 250
    }

    # Mocking database calls
    with patch('app.offices.get_office_by_id', return_value=None):
        response = client.put("/update-office/", json=office_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "No such office to update is found"

def test_get_alternatives_requests():
    mock_requests = [
        {"id": 1, "office_id": 1, "client_id": 2, "status": "Pending"},
        {"id": 2, "office_id": 2, "client_id": 3, "status": "Approved"}
    ]

    # Mocking database calls
    with patch('app.alternatives.get_all_alternatives_service', return_value=mock_requests):
        response = client.get("/alternative/requests/")

        assert response.status_code == 200
        alternatives = response.json()
        assert len(alternatives) == 2
        assert alternatives[0]["status"] == "Pending"

def test_respond_to_alternative_request():
    request_data = {
        "request_id": 1,
        "response": "We can offer a better location for the event."
    }

    # Mocking database calls
    with patch('app.alternatives.send_response_service', return_value=MagicMock(id=1, created_at="2024-12-01T12:00:00")):
        response = client.post("/alternative/respond/1/", json=request_data)

        assert response.status_code == 200
        assert response.json()["message"] == "Response 1 created successfully at 2024-12-01T12:00:00"
