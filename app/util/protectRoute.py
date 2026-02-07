# app/util/protectRoute.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from app.db.models.user import User
from app.core.database import get_db
from sqlalchemy.orm import Session
from decouple import config

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

security = HTTPBearer()

def get_current_user_id(token: str = Depends(security), db: Session = Depends(get_db)) -> int:
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
