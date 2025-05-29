import streamlit as st
import requests

# --- UI Sidebar ---
st.sidebar.header("🔧 Settings")
mode = st.sidebar.radio("Choose Mode:", ["Market Brief", "News Scraper", "Video Player"])

# --- Header ---
st.title("📈 Finance Market Brief Assistant")

if mode == "Market Brief":
    stock_symbol = st.text_input("Stock Symbol (e.g., AAPL)", "AAPL")
    crypto_symbol = st.text_input("Cryptocurrency Symbol (e.g., BTC)", "BTC")

    if st.button("Get Market Brief"):
        if not stock_symbol or not crypto_symbol:
            st.warning("Please enter both stock and cryptocurrency symbols.")
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/market-brief",
                    json={"stock_symbol": stock_symbol, "crypto_symbol": crypto_symbol},
                    timeout=10
                )
                if response.status_code == 200:
                    result = response.json()
                    st.subheader("Market Brief:")
                    if "brief" in result:
                        st.write(result["brief"])
                    elif "error" in result:
                        st.error(result["error"])
                    else:
                        st.write(result)
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {e}")

elif mode == "News Scraper":
    st.info("📰 News Scraper feature coming soon...")

elif mode == "Video Player":
    st.info("🎥 Video Player feature coming soon...")
