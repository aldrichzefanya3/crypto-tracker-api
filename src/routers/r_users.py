from fastapi import APIRouter, Depends, HTTPException
from src.database import SessionLocal
from src.repositories import tokens, users
from sqlalchemy.orm import Session
from src.schemas import s_users, s_coins, s_tokens
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

@router.post("/sign-in/", response_model=s_tokens.Token)
async def login(user: s_users.UserLogin, db: Session = Depends(get_db)):
    user = users.authenticate(db, user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = tokens.generate_access_token(user.email)

    tokens.save_token(db, token=access_token, email=user.email)

    return { "access_token": access_token }

