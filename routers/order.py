from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from config.dabatase import Session
from models.order import Order as OrderModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from schemas.order import Order
from services.order import OrderService
from fastapi import status, Body
from models.user import User
from fastapi import HTTPException
from typing import List
from schemas.movie import MovieCreated
from schemas.order import OrderMovie
from schemas.movie import Movie

order_router = APIRouter()

@order_router.get(
        path='/orders', 
        tags=['orders'], 
        response_model=List[Order],
        status_code=status.HTTP_200_OK,
        summary="Get All Orders")
def get_orders():
    db = Session()
    result = OrderService(db).get_orders()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@order_router.get(
        path='/orders/{id}', 
        tags=['orders'], 
        response_model=Order,
        status_code=status.HTTP_200_OK,
        summary="Get Order By Id")
def get_order_by_id(id: int = Path(...)):
    db = Session()
    result = OrderService(db).get_order_by_Id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@order_router.get(
        path='/orders/movies/{id_order}', 
        tags=['orders'], 
        response_model=List[Movie],
        status_code=status.HTTP_200_OK,
        summary="Get Movies of Order By Id")
def get_order_movies_by_id(id_order: int = Path(...)):
    db = Session()
    result = OrderService(db).get_order_by_Id(id_order)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    result_movies = OrderService(db).get_order_movies_by_id(id_order)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result_movies))

@order_router.post(
        path='/orders/{id_user}',
        tags=['orders'], 
        status_code=status.HTTP_201_CREATED,
        response_model=dict,
        summary="Create a new Order")
def create_order(id_user: int = Path(...), movies: List[MovieCreated] = Body(...)):
    db = Session()
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Create order
    order = Order(user_id=id_user)
    id_order = OrderService(db).create_order(order).id
    # Create OrderMovie
    for i in movies:
        order_movie = OrderMovie(order_id=id_order, movie_id=i.id, quantity=i.quantity)
        OrderService(db).create_order_movie(order_movie)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Order Created"})

@order_router.put(
        path='/orders/{id}',
        tags=['orders'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Update Order")
def update_order(id: int, movies: List[MovieCreated] = Body(...)):
    db = Session()
    result = OrderService(db).get_order_by_Id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    OrderService(db).delete_movies_of_order(id)
    for i in movies:
        order_movie = OrderMovie(order_id=id, movie_id=i.id, quantity=i.quantity)
        OrderService(db).create_order_movie(order_movie)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Se ha modificado el Order"})

@order_router.delete(
        path='/orders/{id}',
        tags=['orders'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Delete Order")
def delete_order(id: int = Path(...)):
    db = Session()
    result = OrderService(db).get_order_by_Id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not Found")
    OrderService(db).delete_order(id)
    OrderService(db).get_order_movies_by_id(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Order removed"})