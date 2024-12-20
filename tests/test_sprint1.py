from unittest import mock

from fastapi.testclient import TestClient
from src.app import app
from unittest.mock import patch
import pytest

client = TestClient(app)

@pytest.fixture
def mock_db():
    with patch('src.database.get_db') as mock:
        yield mock


@pytest.fixture
def mock_get_client_by_email_and_phone():
    with (patch('src.repositories.clients.get_client_by_email') as mock_email,
          patch('src.repositories.clients.get_client_by_phone') as mock_phone):
        yield mock_email, mock_phone


def test_signup_success(mock_db, mock_get_client_by_email_and_phone):
    mock_get_client_by_email, mock_get_client_by_phone = mock_get_client_by_email_and_phone

    mock_get_client_by_email.return_value = None
    mock_get_client_by_phone.return_value = None

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe6@example.com",
        "phone": "333444555666",
        "date_of_birth": "1990-01-01",
        "password": "SecurePassword123"
    }

    response = client.post("/clients/auth/sign-up/", json=data)

    assert response.status_code == 200
    assert "token" in response.json()
    assert response.json()["message"] == "Signup successful"


def test_signup_email_already_registered(mock_db, mock_get_client_by_email_and_phone):
    mock_get_client_by_email_and_phone[0].return_value = {"email": "john.doe@example.com"}
    mock_get_client_by_email_and_phone[1].return_value = None

    data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567891",
        "date_of_birth": "1990-01-01",
        "password": "SecurePassword123"
    }

    response = client.post("/clients/auth/sign-up/", json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_signup_phone_already_registered(mock_db, mock_get_client_by_email_and_phone):
    mock_get_client_by_email_and_phone[0].return_value = None
    mock_get_client_by_email_and_phone[1].return_value = {"phone": "1234567891"}

    data = {
        "name": "John",
        "surname": "Doe",
        "email": "ohn.doe@example.com",
        "phone": "1234567891",
        "date_of_birth": "1990-01-01",
        "password": "SecurePassword123"
    }

    response = client.post("/clients/auth/sign-up/", json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Phone number already registered"

@pytest.fixture
def mock_authenticate_client_phone():
    with patch('src.services.auth_service.authenticate_client_phone') as mock_auth:
        yield mock_auth

def test_login_fail_with_incorrect_phone(mock_authenticate_client_phone):
    mock_authenticate_client_phone.side_effect = Exception("Invalid phone number or password")

    data = {"phone": "1234567890", "password": "SecurePassword123"}

    response = client.post("/clients/auth/sign-in/phone/", json=data)

    assert response.status_code == 400

    assert "detail" in response.json()

@pytest.fixture
def mock_authenticate_client_email():
    with patch('src.routing.client.login_client_email') as mock_auth:
        yield mock_auth

def test_login_success_with_email(mock_authenticate_client_email):
    mock_authenticate_client_email.return_value = "mock_token"

    data = {"email": "john.doe@example.com", "password": "SecurePassword123"}

    response = client.post("/clients/auth/sign-in/email/", json=data)

    assert response.status_code == 200

    assert response.json()["message"] == "Login successful"
    assert "Auth" in response.json()


def test_login_fail_with_incorrect_email(mock_authenticate_client_email):
    mock_authenticate_client_email.side_effect = Exception("Invalid email or password")

    data = {"email": "client@example.com", "password": "SecurePassword123"}

    response = client.post("clients/auth/sign-in/email/", json=data)

    assert response.status_code == 400

    assert "detail" in response.json()
