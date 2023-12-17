from fastapi import APIRouter, Depends, HTTPException
from src.database import SessionLocal
from src.repositories import users
from sqlalchemy.orm import Session
from src.schemas import s_users, s_coins
from src import repositories as db

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not Found"}}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sign-up/", response_model=s_users.User)
async def register_user(user: s_users.UserCreate, db: Session = Depends(get_db)):
    is_user_exists = users.get_user_by_email(db, user.email)
    if is_user_exists:
        raise HTTPException(status_code=404, detail="Email already registered")
    return users.create_user(db, user)

@router.post("/sign-in/")
async def login():
    return {"Code": 200}