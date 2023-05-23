from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.dabatase import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router
from routers.order import order_router
from pydantic import BaseModel
from sqlalchemy import MetaData, Table


app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"
Base.metadata.create_all(bind=engine)
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)
app.include_router(order_router)

@app.get('/', tags=['home'])
def message():
    table_name = 'order_movies'
    table = Table(table_name, Base.metadata, autoload=True, autoload_with=engine)
    table.drop(engine)
    return HTMLResponse('<h1>Hello world</h1>')
