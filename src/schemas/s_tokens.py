from pydantic import BaseModel

class TokenBase(BaseModel):
    email: str

class TokenCreate(TokenBase):
    email: str
    token: str

class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    email: str | None = None