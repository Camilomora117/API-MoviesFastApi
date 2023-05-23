from pydantic import BaseModel, Field

class BaseMovie(BaseModel):
    title: str = Field(min_length=5, max_length=15, example="Mi película")
    overview: str = Field(min_length=15, max_length=50, example="Descripción de la película")
    year: int = Field(le=2022, example=2022)
    rating:float = Field(ge=1, le=10, example=9.8)
    category:str = Field(min_length=5, max_length=15, example="Acción")

class Movie(BaseMovie):
    pass

class MovieCreated(BaseMovie):
    id: int = Field(..., example="1")
    quantity:int = Field(...,ge=1,example="1")

