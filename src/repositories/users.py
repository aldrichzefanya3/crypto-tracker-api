
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt


from src.schemas import s_users, s_tokens
from src.models import m_users

pwd_context = CryptContext(schemes=["bcrypt"])

def get_user(db: Session, user_id: int):
    return db.query(m_users.User).filter(m_users.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(m_users.User).filter(m_users.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(m_users.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: s_users.UserCreate):
    hashed_password = hash_password(user.password)

    db_user = m_users.User(email=user.email, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def authenticate(db: Session, email:str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user