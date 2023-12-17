from pydantic import BaseModel

class CoinBase(BaseModel):
    email: str

class CoinCreate(CoinBase):
    password: str

class Coin(CoinBase):
    id: int
    user_id: int
    coin_name: str
    coin_price: int

    class Config:
        from_attributes = True