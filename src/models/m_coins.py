
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import uuid
from src.database import Base

class Coin(Base):
    __tablename__ = "coins"

    id = Column(String, primary_key=True, index=True, default=uuid.uuid4())
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    coin_name = Column(String, nullable=False)
    coin_price = Column(Integer, nullable=False)

    user = relationship("User", back_populates="coins")

    