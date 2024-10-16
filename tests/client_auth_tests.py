import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_register_client():
    response = client.post("/clients/auth/sign-in/phone",
                           json={"name": "Test",
                                "surname": "User",
                                "email": "testuser@gmail.com",
                                "phone": "8888888888888",
                                "date_of_birth": "2004-12-25",
                                "password": "sdulove2022"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_existing_user():
    client.post("/clients/auth/sign-in/phone",
                json={"name": "Test 2",
                      "surname": "User",
                      "email": "testuser2@gmail.com",
                      "phone": "89999990000",
                      "date_of_birth": "2004-12-25",
                      "password": "sdulove2022"})
    response = client.post("/clients/auth/sign-in/phone",
                json={"name": "Test 2",
                        "surname": "User",
                        "email": "testuser2@gmail.com",
                        "phone": "89999990000",
                        "date_of_birth": "2004-12-25",
                        "password": "sdulove2022"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_login_user():
    client.post("/register", json={"username": "testuser", "password": "testpassword"})
    response = client.post("/login", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

def test_login_wrong_password():
    client.post("/register", json={"username": "testuser", "password": "testpassword"})
    response = client.post("/login", json={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect password"}

def test_login_nonexistent_user():
    response = client.post("/login", json={"username": "nonexistent", "password": "testpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User not found"}
