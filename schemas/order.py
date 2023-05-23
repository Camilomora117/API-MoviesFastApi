from datetime import datetime
from pydantic import BaseModel, Field

class Order(BaseModel):
    date_created: datetime = Field(default=datetime.now())
    user_id: int = Field(..., example="1")

class OrderMovie(BaseModel):
    order_id: int = Field(..., example="1")
    movie_id: int = Field(..., example="1")
    quantity: int = Field(..., example="1")


        





    
