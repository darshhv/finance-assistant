from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging

app = FastAPI(title="News Microservice", version="1.0")

# Enable CORS for frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in prod
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("news_microservice")

NEWS_API_KEY = "895636cfc8a643648d8d1aff0ebe010e"  # Put your key here
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

@app.get("/latest_news")
async def get_latest_news(country: str = "us", category: str = "business"):
    """
    Fetch latest news headlines from NewsAPI.org.
    Defaults: US business news.
    """
    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "category": category,
        "pageSize": 5,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(NEWS_API_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])

            # Simplify article info for frontend
            simplified = [
                {
                    "title": art["title"],
                    "description": art.get("description"),
                    "url": art["url"],
                    "source": art["source"]["name"],
                    "publishedAt": art["publishedAt"],
                }
                for art in articles
            ]

            logger.info(f"Fetched {len(simplified)} news articles")
            return {"articles": simplified}

        except httpx.HTTPStatusError as e:
            logger.error(f"News API HTTP error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=502, detail="Failed to fetch news data from external API")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
