import asyncio
from fastapi import FastAPI, Query, HTTPException
import httpx
import logging
from typing import List, Optional

logger = logging.getLogger("retriever_agent")

app = FastAPI()

API_AGENT_URL = "http://localhost:8000"
SCRAPING_AGENT_URL = "http://localhost:8001"

@app.get("/retrieve_stock_info")
async def retrieve_stock_info(
    symbol: str = Query(..., description="Stock symbol to fetch data for"),
    news_url: Optional[str] = Query("https://www.marketwatch.com/", description="URL to scrape headlines from"),
    news_css_selector: Optional[str] = Query(".collection__elements a.headline", description="CSS selector to extract headlines"),
):
    async with httpx.AsyncClient() as client:
        # Make async requests concurrently
        alpha_vantage_task = client.get(f"{API_AGENT_URL}/alpha_vantage", params={"symbol": symbol})
        finnhub_task = client.get(f"{API_AGENT_URL}/finnhub_quote", params={"symbol": symbol})
        headlines_task = client.get(f"{SCRAPING_AGENT_URL}/headlines", params={"url": news_url, "css_selector": news_css_selector})

        responses = await asyncio.gather(
            alpha_vantage_task, finnhub_task, headlines_task, return_exceptions=True
        )

    alpha_vantage_data, finnhub_data, headlines_data = None, None, None

    # Process AlphaVantage response
    if isinstance(responses[0], Exception):
        logger.error(f"AlphaVantage request failed: {responses[0]}")
    else:
        if responses[0].status_code == 200:
            alpha_vantage_data = responses[0].json()
        else:
            logger.error(f"AlphaVantage returned status code {responses[0].status_code}")

    # Process Finnhub response
    if isinstance(responses[1], Exception):
        logger.error(f"Finnhub request failed: {responses[1]}")
    else:
        if responses[1].status_code == 200:
            finnhub_data = responses[1].json()
        else:
            logger.error(f"Finnhub returned status code {responses[1].status_code}")

    # Process Headlines scraping response
    if isinstance(responses[2], Exception):
        logger.error(f"Headlines request failed: {responses[2]}")
    else:
        if responses[2].status_code == 200:
            headlines_data = responses[2].json()
        else:
            logger.error(f"Headlines returned status code {responses[2].status_code}")

    return {
        "alpha_vantage": alpha_vantage_data,
        "finnhub": finnhub_data,
        "headlines": headlines_data,
    }
