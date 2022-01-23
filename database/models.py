from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.sql.expression import false, true
from .database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True, nullable=false)
    ticker = Column(String, nullable=false)
    buyDate = Column(Date, nullable=true)
    buyAmount = Column(Numeric(10, 2), nullable=true)
    buyFeeEur = Column(Numeric(10, 2), nullable=true)