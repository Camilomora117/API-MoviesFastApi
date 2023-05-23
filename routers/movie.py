from fastapi import APIRouter
from fastapi import Depends, Path, Body, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List
from models.movie import Movie as MovieModel
from schemas.movie import Movie
from services.movie import MovieService
from middlewares.jwt_bearer import JWTBearer
from config.dabatase import Session

movie_router = APIRouter()

@movie_router.get(
        path='/movies', tags=['movies'], 
        response_model=List[Movie], 
        status_code=status.HTTP_200_OK, 
        summary="Get All Movies",
        dependencies=[Depends(JWTBearer())])
def get_movies():
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@movie_router.get(
        path='/movies/{id}', 
        tags=['movies'], 
        response_model=Movie,
        status_code=status.HTTP_200_OK,
        summary="Get movie by id",
        dependencies=[Depends(JWTBearer())])
def get_movie_by_id(id: int = Path(...)):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@movie_router.get(
        path='/movies/category/{category}', 
        tags=['movies'], 
        response_model=List[Movie],
        status_code=status.HTTP_200_OK,
        summary="Get movies by category",
        dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: str = Path(..., min_length=5, max_length=15)):
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@movie_router.post(
        path='/movies', 
        tags=['movies'], 
        response_model=dict, 
        status_code=status.HTTP_201_CREATED,
        summary="Create a new Movie",
        dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie):
    db = Session()
    MovieService(db).create_movie(movie)    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Se ha registrado la película"})

@movie_router.put(
        path='/movies/{id}', 
        tags=['movies'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Update a movie",
        dependencies=[Depends(JWTBearer())])
def update_movie(id: int = Path(...), movie: Movie = Body(...)):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Modified movie"})

@movie_router.delete(
        path='/movies/{id}', 
        tags=['movies'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Delete a movie",
        dependencies=[Depends(JWTBearer())])
def delete_movie(id: int = Path(...)):
    db = Session()
    result: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Movie removed"})