from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging

app = FastAPI(title="Stock Quote Microservice", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to your frontend URL for production
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stock_quote_microservice")

FINNHUB_API_KEY = "d0ro09hr01qumepfe6cgd0ro09hr01qumepfe6d0"
FINNHUB_API_URL = "https://finnhub.io/api/v1/quote"

@app.get("/quote/{symbol}")
async def get_stock_quote(symbol: str):
    """
    Fetch real-time stock quote for given symbol from Finnhub.io.
    """
    params = {
        "symbol": symbol.upper(),
        "token": FINNHUB_API_KEY,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(FINNHUB_API_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            if not data or "c" not in data:
                logger.warning(f"No data found for symbol: {symbol}")
                raise HTTPException(status_code=404, detail="Stock symbol not found")

            # Map Finnhub fields to friendlier keys
            result = {
                "source": f"Finnhub {symbol.upper()} quote",
                "current": data.get("c"),
                "high": data.get("h"),
                "low": data.get("l"),
                "open": data.get("o"),
                "previous_close": data.get("pc"),
            }

            logger.info(f"Fetched quote for symbol: {symbol}")
            return result

        except httpx.HTTPStatusError as e:
            logger.error(f"Finnhub HTTP error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=502, detail="Failed to fetch stock quote from external API")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
