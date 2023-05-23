from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    username: str = Field(...)
    password:str = Field(..., min_length=5)
    email:str = EmailStr(...)

class UserLogin(BaseModel):
    username: str = Field(..., example="camilo")
    password:str = Field(..., min_length=5, example="12345")

class UserSingUp(BaseModel):
    username: str = Field(...)
    email:str = EmailStr(...)
