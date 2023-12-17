from pydantic import BaseModel
from src.schemas.s_coins import Coin

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    email: str
    password: str

class User(UserBase):
    id: int
    coins: list[Coin] = []

    class Config:
        from_attributes = True