
import os
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from src.database import SessionLocal
from src.models.m_users import User
from src.repositories.users import get_user_by_email
from src.models import m_tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

def decode_token(token: Annotated[User, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        
        user = get_user_by_email(db, email=email)

        token_data = get_token_by_user_id(db, user_id=user.id)
        
        if token != token_data.token:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception
    

def delete_token(db: Session, email:str):
    user = get_user_by_email(db, email=email)

    token_data = get_token_by_user_id(db, user_id=user.id)

    if not token_data:
        return
    
    db.delete(token_data)
    db.commit()

    return 
