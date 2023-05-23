from schemas.user import User
from models.user import User as UserModel
from utils.jwt_manager import verify_password

class UserService():
    
    def __init__(self, db) -> None:
        self.db = db

    def authenticate_user(self, user: User):
        result = self.db.query(UserModel).filter(UserModel.username == user.username).first()
        if not result:
            return False
        if not verify_password(user.password, result.password):
            return False
        return True
    
    def get_user_by_Id(self, id):
        result = self.db.query(UserModel).filter(UserModel.id == id).first()
        return result
    
    def get_user_by_username(self, username):
        result = self.db.query(UserModel).filter(UserModel.username == username).first()
        return result

    def create_user(self, user: User):
        new_user = UserModel(**user.dict())
        self.db.add(new_user)
        self.db.commit()
        return new_user
    
    def delete_user(self, id: int):
       self.db.query(UserModel).filter(UserModel.id == id).delete()
       self.db.commit()
       return
    
    def update_user(self, id: int, data: User):
        user = self.db.query(UserModel).filter(UserModel.id == id).first()
        user.username = data.username
        user.email = data.email
        self.db.commit()
        return
    
    def delete_user_by_email(self, email: str):
       self.db.query(UserModel).filter(UserModel.email == email).delete()
       self.db.commit()
       return
