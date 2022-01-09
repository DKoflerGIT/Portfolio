from numpy.core import numeric
from pydantic import BaseModel
from typing import Optional

class StockRequest(BaseModel):
    ticker: str
    buyPrice: Optional[float] = 0
    buyAmount: Optional[float] = 0
    buyFeeEur: Optional[float] = 0