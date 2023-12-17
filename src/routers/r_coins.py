from fastapi import APIRouter, Depends, HTTPException
from src.database import SessionLocal
from sqlalchemy.orm import Session
from src.models.m_users import User
from src.repositories import coins, tokens
from src.schemas import s_coins
from src.utils.api_consumer import hit_api_coin_asset_by_id

router = APIRouter(
    prefix="/my-coin",
    tags=["coin"],
    responses={404: {"description": "Not Found"}}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add/{coin_id}", response_model=s_coins.Coin)
async def add_coin(coin_id: str, current_user: User = Depends(tokens.decode_token), db: Session = Depends(get_db)):
    user_id = current_user.id
    
    get_coin = hit_api_coin_asset_by_id(f"{"v2/assets/"}{coin_id}")

    if not get_coin:
        raise HTTPException(
            status_code=404,
            detail="Coin Not Found",
        )
    
    coin = get_coin.get("data", {})

    coin_name = coin.get("name")
    coin_price = coin.get("priceUsd")

    coin_data = {
        "coin_name": coin_name,
        "coin_price": coin_price
    }

    coin = coins.get_coin_by_email_and_coin_name(db, user_id=user_id, coin_name=coin_name)

    if coin:
        raise HTTPException(status_code=404, detail="Coin Has Been Added")

    add_coin = coins.create_coin(db, coin_data, user_id)

    return add_coin

@router.delete("/remove/{id}")
async def remove_coin(id: str, current_user: User = Depends(tokens.decode_token), db: Session = Depends(get_db)):
    coin_data = coins.delete_coin(db, id)

    if not coin_data:
        raise HTTPException(status_code=404, detail="Coin Not Found")

    return { "detail": "Coin Has Been Removed" }

