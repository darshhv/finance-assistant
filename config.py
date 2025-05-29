from dotenv import load_dotenv
import os

load_dotenv()  # load env vars from .env file in project root

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")