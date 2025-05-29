import os
import uuid
import shutil
import streamlit as st
import requests
from datetime import datetime
from gtts import gTTS
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import queue
import numpy as np
import google.generativeai as genai

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure keys and Gemini
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Check available models
try:
    models = genai.list_models()
except Exception as e:
    models = []
st.write("Available Gemini models:", models)

# Choose a valid Gemini model or fallback
valid_models = [m.name for m in models]
model_name = "models/text-bison-001" if "models/text-bison-001" in valid_models else valid_models[0] if valid_models else None

if not model_name:
    st.error("No valid Gemini models found! Cannot generate summaries.")
else:
    model = genai.GenerativeModel(model_name)

# Setup tmp folder for audio files
TMP_AUDIO_DIR = "./tmp_audio"
os.makedirs(TMP_AUDIO_DIR, exist_ok=True)

# Clear old temp files on start (optional, to avoid clutter)
for f in os.listdir(TMP_AUDIO_DIR):
    try:
        os.remove(os.path.join(TMP_AUDIO_DIR, f))
    except:
        pass

# Audio queue for mic input (basic)
audio_queue = queue.Queue()

class AudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        audio = frame.to_ndarray(format="flt32")
        # Put audio data in queue for future processing (optional)
        audio_queue.put(audio)
        return frame

def speak_text(text: str):
    filename = os.path.join(TMP_AUDIO_DIR, f"voice_{uuid.uuid4()}.mp3")
    tts = gTTS(text)
    tts.save(filename)
    st.audio(filename, format="audio/mp3")

def fetch_market_data(symbol: str, source: str) -> dict:
    try:
        if source == "alphavantage":
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}"
            r = requests.get(url)
            data = r.json().get("Global Quote", {})
            return {
                "symbol": symbol,
                "current": float(data.get("05. price", 0)),
                "open": float(data.get("02. open", 0)),
                "high": float(data.get("03. high", 0)),
                "low": float(data.get("04. low", 0)),
                "previous_close": float(data.get("08. previous close", 0)),
                "timestamp": datetime.now().timestamp()
            }
        else:
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
            r = requests.get(url)
            data = r.json()
            return {
                "symbol": symbol,
                "current": data.get("c", 0),
                "open": data.get("o", 0),
                "high": data.get("h", 0),
                "low": data.get("l", 0),
                "previous_close": data.get("pc", 0),
                "timestamp": datetime.now().timestamp()
            }
    except Exception as e:
        return {"error": str(e)}

def fetch_latest_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API_KEY}"
        r = requests.get(url)
        return r.json().get("articles", [])
    except Exception as e:
        return []

def summarize_with_gemini(prompt):
    if not model_name:
        return "No Gemini model available."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini failed: {e}"

# Streamlit UI
st.title("🎤 Multi-Agent Finance Assistant with Mic & Gemini")

with st.sidebar:
    source = st.selectbox("Select Market Data Source", ["finnhub", "alphavantage"])
    st.markdown("---")
    enable_tts = st.checkbox("Enable Speech Playback", value=True)
    st.markdown("---")
    mic_on = st.checkbox("Enable Microphone Input (Basic)", value=True)

if mic_on:
    webrtc_streamer(
        key="mic-stream",
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

query = st.text_input("Enter stock symbols (comma separated), or your query")

if st.button("Fetch Market Data & Summary"):
    if not query.strip():
        st.warning("Please enter some stock symbols or query")
    else:
        symbols = [s.strip().upper() for s in query.split(",") if s.strip()]
        for symbol in symbols:
            with st.spinner(f"Fetching data for {symbol}..."):
                data = fetch_market_data(symbol, source)
                if "error" in data:
                    st.error(f"Error fetching {symbol}: {data['error']}")
                    continue
                st.markdown(f"### {symbol}")
                st.table({
                    "Symbol": data["symbol"],
                    "Current": f"${data['current']:.2f}",
                    "Open": f"${data['open']:.2f}",
                    "High": f"${data['high']:.2f}",
                    "Low": f"${data['low']:.2f}",
                    "Previous Close": f"${data['previous_close']:.2f}",
                })
                if enable_tts:
                    speak_text(
                        f"{symbol} is trading at ${data['current']:.2f}. "
                        f"Open: {data['open']:.2f}, High: {data['high']:.2f}, "
                        f"Low: {data['low']:.2f}, Previous Close: {data['previous_close']:.2f}."
                    )

        # Gemini summary of all symbols
        prompt = f"Provide a short financial summary for these stocks: {', '.join(symbols)}."
        summary = summarize_with_gemini(prompt)
        st.markdown("### 🧠 AI Summary")
        st.write(summary)
        if enable_tts:
            speak_text(summary)

st.markdown("---")
st.markdown("### 📰 Latest Business News")
articles = fetch_latest_news()
if not articles:
    st.info("No news available right now.")
else:
    for art in articles[:5]:
        st.markdown(f"**{art.get('title')}**  \n{art.get('description','')}  \n[Read more ▶]({art.get('url')})")
        st.markdown("---")
