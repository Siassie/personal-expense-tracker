from app.db.repository.userRepo import UserRepository
from app.db.schema.user import UserOutput, UserInCreate, UserInLogin, UserWithToken
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException

class UserService:
    def __init__(self, session : Session):
        self.__userRepository = UserRepository(session=session)
    

    def sign_up(self, user_details : UserInCreate) -> UserOutput:
        if self.__userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400, detail="User Already exist with provided email. Please login.")
        
        hashed_password = HashHelper.hash_password(plain_text=user_details.password)

        user_details.password = hashed_password

        return self.__userRepository.create_user(user_data=user_details)
    

    def login(self, login_details : UserInLogin) -> UserWithToken:
        if not self.__userRepository.get_user_by_email(email=login_details.email):
            raise HTTPException(status_code=400, detail="User does not exist. Please create an account.")
        
        user = self.__userRepository.get_user_by_email(email = login_details.email)

        if HashHelper.verify_password(plain_text=login_details.password, hashed_password=user.password):
            token = AuthHandler.sign_jwt(user_id=user.id)

            if token:
                return UserWithToken(token=token)
            
            else:
                raise HTTPException(status_code=500, detail="Unable to process request.")
                        
        else:
            raise HTTPException(status_code=400, detail="Password incoreect.")
        
    
    def get_user_by_id(self, user_id : int):
        user = self.__userRepository.get_user_by_id(user_id=user_id)

        if user:
            return user
        
        raise HTTPException(status_code=400, detail="User is not found.")