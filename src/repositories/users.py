from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.schemas import s_users
from src.models import m_users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def authenticate():
    return

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item