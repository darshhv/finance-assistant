import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query

logger = logging.getLogger("scraping_agent")

class ScrapingAgent:
    def __init__(self, user_agent: Optional[str] = None):
        self.headers = {"User-Agent": user_agent} if user_agent else {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def fetch_headlines(self, url: str, css_selector: str) -> Optional[List[str]]:
        try:
            logger.info(f"Fetching headlines from: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.select(css_selector)
            headlines = [el.get_text(strip=True) for el in elements]
            logger.info(f"Fetched {len(headlines)} headlines")
            return headlines
        except requests.RequestException as e:
            logger.error(f"Error fetching headlines: {e}")
            return None


app = FastAPI()
scraper = ScrapingAgent()


@app.get("/headlines")
def get_headlines(url: str = Query(..., description="URL to scrape"),
                  css_selector: str = Query(..., description="CSS selector to extract data")):
    headlines = scraper.fetch_headlines(url, css_selector)
    if headlines is None:
        raise HTTPException(status_code=502, detail="Failed to fetch headlines")
    return {"headlines": headlines}
