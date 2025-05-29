from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import logging
import os
import requests

# Load environment variables from .env
load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "demo")  # Replace 'demo' with your key or keep as default for testing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("finance_backend")

# Initialize FastAPI app
app = FastAPI(
    title="Finance Assistant Backend",
    version="1.0",
    description="Multi-Agent Financial Assistant API"
)

# CORS setup for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ScrapeRequest(BaseModel):
    url: str
    css_selector: str

class RetrievalRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

# Dummy Agents — Replace with real logic or modules
class ApiAgent:
    async def fetch_alpha_vantage(self, symbol):
        # Dummy response for AlphaVantage
        if symbol.upper() == "AAPL":
            return {
                "symbol": "AAPL",
                "price": 150,
                "open": 148,
                "high": 152,
                "low": 147,
                "previous_close": 149,
                "current": 150
            }
        return None

    async def fetch_finnhub_quote(self, symbol):
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if not data or data.get("c") == 0:
                return None
            return {
                "symbol": symbol.upper(),
                "current": data["c"],
                "open": data["o"],
                "high": data["h"],
                "low": data["l"],
                "previous_close": data["pc"]
            }
        except Exception as e:
            logger.error(f"Error fetching Finnhub quote: {e}")
            return None

class ScrapingAgent:
    def fetch_headlines(self, url, css_selector):
        return [
            {"title": "Market rises amid optimism", "description": "Stocks rally due to positive earnings.", "url": "https://news.example.com/market1"},
            {"title": "Crypto hits new highs", "description": "Bitcoin and Ethereum surge.", "url": "https://news.example.com/crypto1"},
        ]

class RetrieverAgent:
    def __init__(self, client):
        self.client = client

    def retrieve(self, query, top_k=5):
        return [{"doc": "Financial report Q1", "score": 0.95}]

class VoiceAgent:
    def listen(self):
        return "Simulated voice command"

    def speak(self, text):
        print(f"Speaking: {text}")

# Initialize agents
api_agent = ApiAgent()
scraper_agent = ScrapingAgent()
retriever_agent = RetrieverAgent(client=None)
voice_agent = VoiceAgent()

# API Routes

@app.get("/")
async def root():
    return {"message": "✅ Finance Assistant API is live"}

@app.get("/stock/alphavantage")
async def get_alpha_vantage_data(symbol: str = Query(..., min_length=1)):
    data = await api_agent.fetch_alpha_vantage(symbol)
    if not data:
        raise HTTPException(status_code=404, detail="No data found from AlphaVantage.")
    return data

@app.get("/stock/finnhub")
async def get_finnhub_quote(symbol: str = Query(..., min_length=1)):
    data = await api_agent.fetch_finnhub_quote(symbol)
    if not data:
        raise HTTPException(status_code=404, detail="No quote found from Finnhub.")
    return data

@app.post("/scrape/headlines")
def scrape_headlines(req: ScrapeRequest):
    headlines = scraper_agent.fetch_headlines(req.url, req.css_selector)
    if not headlines:
        raise HTTPException(status_code=500, detail="Failed to fetch headlines.")
    return {"headlines": headlines}

@app.post("/retrieve")
def retrieve_info(req: RetrievalRequest):
    if not retriever_agent.client:
        raise HTTPException(status_code=503, detail="Vector DB not configured.")
    results = retriever_agent.retrieve(req.query, req.top_k)
    return {"results": results}

@app.get("/voice/listen")
def listen_voice():
    try:
        command = voice_agent.listen()
        return {"transcription": command}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice input failed: {e}")

@app.get("/voice/speak")
def speak_text(text: str):
    try:
        voice_agent.speak(text)
        return {"status": "Spoken successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-to-speech failed: {e}")
