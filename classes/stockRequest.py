from datetime import date
import datetime
from numpy.core import numeric
from pydantic import BaseModel
from typing import Optional

class StockRequest(BaseModel):
    ticker: str
    buyDate: Optional[date] = None
    buyAmount: Optional[float] = 0
    buyFeeEur: Optional[float] = 0