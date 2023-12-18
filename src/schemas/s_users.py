from pydantic import BaseModel


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    email: str
    password: str

class UserLogin(UserBase):
    email: str
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True