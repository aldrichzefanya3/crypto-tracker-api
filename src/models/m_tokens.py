
import uuid

from sqlalchemy import Column, Integer, String

from src.database import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(String, primary_key=True, index=True, default=uuid.uuid4().hex)
    user_id = Column(Integer)
    token = Column(String)
