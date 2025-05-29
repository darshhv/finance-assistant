from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

class MarketBriefRequest(BaseModel):
    stock_symbol: str

@router.post("/market-brief")
def market_brief(req: MarketBriefRequest):
    # Simulate market brief generation
    fake_price = round(random.uniform(100, 500), 2)
    fake_change = f"{random.choice(['+', '-'])}{round(random.uniform(0.1, 5), 2)}%"

    brief_text = f"""
    Stock symbol {req.stock_symbol.upper()} closed at ${fake_price} today with a change of {fake_change}.
    Market sentiment remains cautiously optimistic amid mixed economic signals.
    """

    return {
        "stock_symbol": req.stock_symbol.upper(),
        "stock_price": fake_price,
        "stock_change_percent": fake_change,
        "brief": brief_text.strip()
    }
