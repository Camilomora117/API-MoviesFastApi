from fastapi import Body, status, Path, Depends
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from schemas.user import User, UserLogin, UserSingUp
from services.user import UserService
from middlewares.jwt_bearer import JWTBearer
from utils.jwt_manager import get_password_hash
from utils.jwt_manager import create_token
from config.dabatase import Session

user_router = APIRouter()

@user_router.post(
          path="/login", 
          status_code=status.HTTP_200_OK,
          tags=["users"],
          summary="Login user in the app",
          response_model=dict)
def login(user: UserLogin = Body(...)):
     db = Session()
     result = UserService(db).authenticate_user(user)
     if result:
        token: str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)

@user_router.post(
        path="/signup",
        response_model=UserLogin,
        tags=["users"],
        status_code=status.HTTP_201_CREATED,
        summary="Create new User")
def signup(user: User = Body(...)):
      db = Session()
      existing_user = UserService(db).get_user_by_username(user.username)
      if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
      hashed_password = get_password_hash(user.password)
      user.password = hashed_password
      result = UserService(db).create_user(user)
      signup_user = UserSingUp(username=result.username, email=result.email)
      return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(signup_user))

@user_router.delete(
        path='/users/{id_user}',
        tags=['users'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Delete User",
        dependencies=[Depends(JWTBearer())])
def delete_user(id_user: int = Path(...)):
    db = Session()
    user = UserService(db).get_user_by_Id(id_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    UserService(db).delete_user(id_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User removed"})

@user_router.put(
        path='/users/{id_user}', 
        tags=['users'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Update data User",
        dependencies=[Depends(JWTBearer())])
def update_user(id_user: int = Path(...), user: User = Body(...)):
    db = Session()
    result = UserService(db).get_user_by_Id(id_user)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    UserService(db).update_user(id_user, user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Modified User"})
