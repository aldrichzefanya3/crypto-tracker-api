from pydantic import BaseModel

from src.schemas.s_users import User


class CoinBase(BaseModel):
    id: str
    coin_name: str
    coin_price: float

class CoinCreate(CoinBase):
    pass

class Coin(CoinBase):
    user: User

    class Config:
        from_attributes = True

class ListCoin(BaseModel):
    data: list[Coin]