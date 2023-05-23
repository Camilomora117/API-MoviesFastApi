# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path
from fastapi import status, Form, Header, Cookie, UploadFile, File
from fastapi import HTTPException

app = FastAPI()

# Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The city where the person lives",
        example="New York",
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The state where the person lives",
        example="New York",
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The country where the person lives",
        example="United States",
    )

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Miguel"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Gonzalez"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.brown)
    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase):
    password: str = Field(..., min_length=8)

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='camilomora117')
    password: str = Field(..., min_length=2, max_length=20, example='12345')
    message: str = Field(default='Login successful :)', description='Description message')

@app.get(
        path="/",
        status_code=status.HTTP_200_OK,
        tags=["Home"])
def home():
    return {"Hello": "World!"}

# Request and Response Body
@app.post(
        path="/person/new",
        response_model=PersonOut,
        status_code=status.HTTP_201_CREATED,
        tags=["Persons"],
        summary="Create new Person in app")
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates persons in the app and save in database

    Parameters:
    - Request body:
        ** Person: person** -> A person model

    return a person model 
    """
    return person

# Validaciones: Query Parameters
@app.get(
        path="/person/detail",
        status_code=status.HTTP_200_OK,
        tags=["Persons"])
def show_person(
    name: Optional[str] = Query(
        None, min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name,  It's between 1 and 50 characters",
        example="Rocio"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age, It's required",
        example="25"
        )
):
    return {name: age}

# Validaciones Path Paremeters
persons = [1, 2, 3, 4, 5]
@app.get(
        path="/person/detail/{person_id}",
        status_code=status.HTTP_200_OK,
        tags=["Persons"])
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
    )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encuentra esta persona"
        )
    return {person_id: "It exists!"}

# Validaciones: Request Body
@app.put(
        path="/person/{person_id}",
        status_code=status.HTTP_200_OK,
        tags=["Persons"])
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person


@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(username: str = Form(...), password=Form(...)):
    return LoginOut(username=username, password=password)

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=["Contact"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example='Camilo'
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example='Mora'
    ),
    email: EmailStr = Form(
        ...,
        example='camilo@gmail.com'
    ),
    message: str = Form(
        ...,
        min_length=20,
        max_length=280,
        example='Hola, estoy interesado en tu proyecto'
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'message': message,
        'user_agent': user_agent,
        'ads': ads
    }

@app.post(
    path='/post-image',
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }


