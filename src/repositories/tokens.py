
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from src.repositories.users import get_user_by_email
from src.schemas import s_tokens
from src.models import m_tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_access_token(email:str):
    data = {
        "sub": email
    }

    encode_data = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=15)
    
    encode_data.update({"exp": expire})
    encoded_jwt = jwt.encode(encode_data, os.getenv("JWT_SECRET_KEY"), os.getenv("JWT_ALGORITHM"))

    return encoded_jwt

def get_token_by_user_id(db: Session, user_id: int):
    return db.query(m_tokens.Token).filter(m_tokens.Token.user_id == user_id).first()

def save_token(db: Session, token: str, email: str):
    user = get_user_by_email(db, email=email)

    token_data = get_token_by_user_id(db, user_id=user.id)

    if token_data:
        token_data.token = token
        db.commit()
        db.refresh(token_data)

        return token
    
    db_token = m_tokens.Token(user_id=user.id, token=token)
    
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token
