import httpx
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from config import ALPHAVANTAGE_API_KEY, FINNHUB_API_KEY

logger = logging.getLogger("api_agent")

class ApiAgent:
    ALPHAVANTAGE_BASE_URL = "https://www.alphavantage.co/query"
    FINNHUB_QUOTE_URL = "https://finnhub.io/api/v1/quote"

    def __init__(self):
        if not ALPHAVANTAGE_API_KEY or not FINNHUB_API_KEY:
            logger.warning("API keys not loaded correctly")

    async def fetch_alpha_vantage(self, symbol: str) -> Optional[Dict[str, Any]]:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol.upper(),
            "interval": "5min",
            "apikey": ALPHAVANTAGE_API_KEY,
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.ALPHAVANTAGE_BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                logger.info(f"AlphaVantage data fetched for {symbol}")
                return data
            except httpx.HTTPError as e:
                logger.error(f"AlphaVantage HTTP error for {symbol}: {e}")
                return None

    async def fetch_finnhub_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        params = {"symbol": symbol.upper(), "token": FINNHUB_API_KEY}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.FINNHUB_QUOTE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Finnhub quote fetched for {symbol}")
                return data
            except httpx.HTTPError as e:
                logger.error(f"Finnhub HTTP error for {symbol}: {e}")
                return None


app = FastAPI()
api_agent = ApiAgent()


@app.get("/alpha_vantage")
async def get_alpha_vantage(symbol: str = Query(..., description="Stock symbol")):
    data = await api_agent.fetch_alpha_vantage(symbol)
    if data is None:
        raise HTTPException(status_code=502, detail="Failed to fetch data from AlphaVantage")
    return data


@app.get("/finnhub_quote")
async def get_finnhub_quote(symbol: str = Query(..., description="Stock symbol")):
    data = await api_agent.fetch_finnhub_quote(symbol)
    if data is None:
        raise HTTPException(status_code=502, detail="Failed to fetch data from Finnhub")
    return data
