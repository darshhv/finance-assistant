from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.api_agent import generate_market_brief

app = FastAPI()

# Allow requests from all origins (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MarketRequest(BaseModel):
    stock_symbol: str
    crypto_symbol: str

@app.post("/market-brief")
async def market_brief(request: MarketRequest):
    result = generate_market_brief(request.stock_symbol, request.crypto_symbol)
    return result
