from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from utils.jwt_manager import validate_token
from schemas.user import User
from services.user import UserService
from config.dabatase import Session

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        db = Session()
        result = UserService(db).authenticate_user(User(**data))
        if not result:
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")