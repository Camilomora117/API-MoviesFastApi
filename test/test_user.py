from fastapi.testclient import TestClient
from security import app
from fastapi import status
from schemas.user import UserSingUp
from config.dabatase import Session
from services.user import UserService
import pytest
from utils.jwt_manager import create_token

credentials = {"username": "prueba", "password": "prueba", "email": "prueba@gmail.com"}

def get_token():
    token = create_token(credentials)
    return token

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client
    db = Session()
    UserService(db).delete_user_by_email("prueba@gmail.com")

@pytest.fixture(scope="module")
def test_user():
    return credentials
    
def test_signup_create_user(test_client, test_user):
    response = test_client.post("/signup", json=test_user)
    signup_user = UserSingUp(username=test_user["username"], email=test_user["email"])
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == signup_user

def test_signup_user_already_exists(test_client, test_user):
    response = test_client.post("/signup", json=test_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User already exists"}

def test_login_user(test_client, test_user):
    data = {"username": test_user["username"], "password":test_user["password"]}
    response = test_client.post("/login", json=data)
    assert response.status_code == status.HTTP_200_OK

def test_delete_user_not_found(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.delete("/users/2000", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}

def test_update_user_not_found(test_client, test_user):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.put("/users/2000", json=test_user, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}

def test_delete_access_forbidden(test_client):
    response = test_client.delete("/users/2000")
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_update_access_forbidden(test_client, test_user):
    response = test_client.put("/users/2000", json=test_user)
    assert response.status_code == status.HTTP_403_FORBIDDEN

