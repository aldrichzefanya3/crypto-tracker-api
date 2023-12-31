from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from src.models import m_coins


def create_coin(db: Session, coin_data: dict, user_id: str):
    coin_name = coin_data.get("coin_name")
    coin_price = coin_data.get("coin_price")
    
    db_coin = m_coins.Coin(user_id=user_id,coin_name=coin_name, coin_price=coin_price)

    db.add(db_coin)
    db.commit()
    db.refresh(db_coin)

    return db_coin

def get_coins(db: Session, user_id: int, page: int, per_page: int):
    skip: int = (page - 1) * per_page
    limit: int = per_page

    return db.query(m_coins.Coin).filter(m_coins.Coin.user_id == user_id).options(joinedload(m_coins.Coin.user)).offset(skip).limit(limit).all()

def get_coin_by_id(db: Session, id: int):
    return db.query(m_coins.Coin).filter(m_coins.Coin.id == id).first()

def get_coin_by_email_and_coin_name(db: Session, user_id: int, coin_name:str):
    return db.query(m_coins.Coin).filter(m_coins.Coin.user_id == user_id, m_coins.Coin.coin_name == coin_name).first()

def delete_coin(db: Session, id: int):
    coin = get_coin_by_id(db, id=id)

    if not coin:
        raise HTTPException(status_code=404, detail="Coin Not Found")
    
    db.delete(coin)
    db.commit()

    return