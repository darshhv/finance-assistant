import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Multi-Agent Finance Assistant",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS for design
st.markdown("""
    <style>
    .stApp { font-family: 'Arial', sans-serif; color: #333; }
    .header-title { font-size: 2.5rem; font-weight: 700; margin-bottom: 0; }
    .header-subtitle { font-size: 1.2rem; color: #555; margin-top: 0; margin-bottom: 1.5rem; }
    .mic-button > button {
        font-size: 2rem;
        padding: 1rem;
        border-radius: 50%;
        background-color: #4CAF50;
        color: white;
    }
    .mic-button > button:focus { outline: 3px solid #FFEB3B; }
    .listening { color: #E53935; font-weight: bold; animation: pulse 1s infinite; }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .news-container {
        max-height: 300px;
        overflow-y: auto;
        padding-right: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Functions
def fetch_market_data(symbol: str, source: str = "finnhub") -> dict:
    url = f"http://127.0.0.1:8000/stock/{source}?symbol={symbol}"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()

def fetch_latest_news() -> list:
    url = "http://127.0.0.1:8001/latest_news"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json().get("articles", [])

def speak_text(text: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

# Session States
if "listening" not in st.session_state:
    st.session_state.listening = False
if "query" not in st.session_state:
    st.session_state.query = ""
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
if "source" not in st.session_state:
    st.session_state.source = "finnhub"

# Header
st.markdown('<h1 class="header-title">💹 Multi-Agent Finance Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtitle">Speak or type to get real-time market briefs and latest financial news.</p>', unsafe_allow_html=True)

# Input UI
col1, col2, col3 = st.columns([1, 4, 2], gap="small")

with col1:
    st.markdown('<div class="mic-button">', unsafe_allow_html=True)
    if st.button("🎙️"):
        st.session_state.listening = True
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio_placeholder = st.empty()
            audio_placeholder.markdown('<p class="listening">Listening...</p>', unsafe_allow_html=True)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            audio_placeholder.empty()
        try:
            text = recognizer.recognize_google(audio)
            st.session_state.query = text
            st.session_state.query_input = text
        except Exception:
            st.error("Voice recognition failed. Please try again.")
        st.session_state.listening = False
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.text_input(
        "Enter your question or symbol(s)",
        placeholder="e.g. AAPL, TSLA, BTC",
        key="query_input",
        on_change=lambda: st.session_state.update({"query": st.session_state.query_input})
    )

with col3:
    st.selectbox("Select Data Source", ["finnhub", "alphavantage"], key="source")

# Results
if st.session_state.query:
    st.markdown("### 🧠 Your Query")
    st.write(st.session_state.query)

    symbols = [s.strip().upper() for s in st.session_state.query.split(",") if s.strip()]
    st.markdown("### 📊 Market Brief Response")

    for symbol in symbols:
        try:
            with st.spinner(f"Fetching market data for {symbol}..."):
                data = fetch_market_data(symbol, st.session_state.source)

            with st.container():
                st.markdown(f"**{symbol}**")
                market_info = {
                    "Symbol": data.get("symbol", "").upper(),
                    "Current": f"${data.get('current', 0):,.2f}",
                    "Open": f"${data.get('open', 0):,.2f}",
                    "High": f"${data.get('high', 0):,.2f}",
                    "Low": f"${data.get('low', 0):,.2f}",
                    "Previous Close": f"${data.get('previous_close', 0):,.2f}",
                }
                st.table(market_info)

                ts = data.get("timestamp")
                if ts:
                    st.caption(f"Last updated: {datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}")

                if st.session_state.tts_enabled:
                    speech_text = (
                        f"{symbol} current price is {data.get('current')} dollars. "
                        f"High {data.get('high')}, low {data.get('low')}, open {data.get('open')}, "
                        f"previous close {data.get('previous_close')}."
                    )
                    speak_text(speech_text)

        except requests.HTTPError as e:
            st.error(f"Failed to fetch market data for {symbol}: {e}")
        except Exception as e:
            st.error(f"Unexpected error fetching data for {symbol}: {e}")

    st.checkbox("🔊 Enable Speech Playback", value=st.session_state.tts_enabled, key="tts_enabled")

# News Section
st.markdown("---")
st.markdown("### 🗞️ Latest Market News")
try:
    with st.spinner("Loading latest news..."):
        articles = fetch_latest_news()

    if not articles:
        st.info("No news available at the moment.")
    else:
        st.markdown('<div class="news-container">', unsafe_allow_html=True)
        for art in articles:
            title = art.get("title", "No title")
            desc = art.get("description") or "No description available."
            url = art.get("url", "#")
            st.markdown(f"**{title}**  \n{desc}  \n[Read more ▶]({url})\n\n---")
        st.markdown('</div>', unsafe_allow_html=True)

except requests.HTTPError as e:
    st.error(f"Failed to load news: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
