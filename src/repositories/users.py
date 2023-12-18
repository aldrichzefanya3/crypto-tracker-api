
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.models import m_users
from src.schemas import s_users

pwd_context = CryptContext(schemes=["bcrypt"])

def get_user_by_email(db: Session, email: str):
    return db.query(m_users.User).filter(m_users.User.email == email).first()

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

def authenticate(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user