from fastapi.testclient import TestClient
from security import app
from fastapi import status
from schemas.user import UserSingUp
from config.dabatase import Session
from services.user import UserService
import pytest
from utils.jwt_manager import create_token

credentials = {"username": "prueba", "password": "prueba", "email": "prueba@gmail.com"}

movie = {
        "title": "Test Pelicula",
        "overview": "Descripción de la película",
        "year": 2022,
        "rating": 9.8,
        "category": "CategoryTest"
        }

id_movie_global = 0

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

@pytest.fixture(scope="module")
def test_movie():
    return movie

def test_create_test_for_tests(test_client, test_user):
    test_client.post("/signup", json=test_user)

def test_create_movie_successfully(test_client, test_movie):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.post("/movies", json=test_movie,headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "Se ha registrado la película"}

def test_get_movies_status_code(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.get("/movies", headers=headers)
    global id_movie_global
    id_movie_global = int(response.json()[-1]['id'])
    assert response.status_code == status.HTTP_200_OK

def test_update_movie_not_found(test_client, test_movie):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.put("/movies/1000", headers=headers, json=test_movie)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Movie not found"}

def test_update_movie_successfully(test_client, test_movie):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.put("/movies/" + str(id_movie_global), headers=headers, json=test_movie)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Modified movie"}

def test_get_movie_by_id_successfully(test_client, test_movie):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.get("/movies/" + str(id_movie_global), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == test_movie["title"]
    assert response.json()["overview"] == test_movie["overview"]
    assert response.json()["year"] == test_movie["year"]
    assert response.json()["rating"] == test_movie["rating"]
    assert response.json()["category"] == test_movie["category"]

def test_get_movie_by_category_successfully(test_client, test_movie):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.get("/movies/category/" + test_movie["category"], headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["title"] == test_movie["title"]
    assert response.json()[0]["overview"] == test_movie["overview"]
    assert response.json()[0]["year"] == test_movie["year"]
    assert response.json()[0]["rating"] == test_movie["rating"]
    assert response.json()[0]["category"] == test_movie["category"]

def test_get_movie_by_id_not_found(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.get("/movies/1000", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Movie not found"}

def test_delete_movie_successfully(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.delete("/movies/" + str(id_movie_global), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Movie removed"}

def test_delete_movie_not_found(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.delete("/movies/1000", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Movie not found"}