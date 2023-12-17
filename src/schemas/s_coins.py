from pydantic import BaseModel

class CoinBase(BaseModel):
    coin_name: str
    coin_price: int

class CoinCreate(CoinBase):
    pass

class Coin(CoinBase):
    id: str
    user_id: int
    coin_name: str
    coin_price: float

    class Config:
        from_attributes = True