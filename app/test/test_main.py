from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/healthy")
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy"}

def test_register_user():
    response = client.post("/auth/register", json={
        "username": "testuser123",
        "email": "testuser123@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test123",
        "role": "user",
        "phone_number": "9999999999"
    })
    assert response.status_code == 201

def test_register_duplicate_user():
    client.post("/auth/register", json={
        "username": "dupuser123",
        "email": "dupuser123@gmail.com",
        "first_name": "Dup",
        "last_name": "User",
        "password": "test123",
        "role": "user",
        "phone_number": "7777777777"
    })
    response = client.post("/auth/register", json={
        "username": "dupuser123",
        "email": "dupuser123@gmail.com",
        "first_name": "Dup",
        "last_name": "User",
        "password": "test123",
        "role": "user",
        "phone_number": "7777777777"
    })
    assert response.status_code == 400

def test_login_user():
    client.post("/auth/register", json={
        "username": "logintest123",
        "email": "logintest123@gmail.com",
        "first_name": "Login",
        "last_name": "Test",
        "password": "test123",
        "role": "user",
        "phone_number": "8888888888"
    })
    response = client.post("/auth/token", data={
        "username": "logintest123",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/auth/token", data={
        "username": "logintest123",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_incidents_without_auth():
    response = client.get("/incidents/")
    assert response.status_code == 401

def test_get_dashboard_without_auth():
    response = client.get("/incidents/dashboard")
    assert response.status_code == 401

def test_delete_incident_without_auth():
    response = client.delete("/incidents/1")
    assert response.status_code == 401