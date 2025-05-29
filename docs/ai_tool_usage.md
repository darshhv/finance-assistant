# AI Tool Usage Documentation

## Overview
This document provides a detailed log of the AI tool prompts, code generation steps, and model parameters used during the development of the Multi-Agent Finance Assistant project. It also includes demo videos and GIFs illustrating voice and text interaction workflows.

---

## 1. AI Prompts and Interaction Log

### Initial Prompts
- Designed a Streamlit app integrating multi-source finance APIs (Finnhub, AlphaVantage).
- Added voice assistant capabilities with `gTTS` for speech synthesis.
- Included microphone audio capture using `streamlit_webrtc`.

### Code Generation Highlights
- Implementation of real-time stock quote fetching with Finnhub and AlphaVantage.
- Use of `@st.cache_data` decorator to cache API responses and optimize performance.
- Integration of keyword-triggered voice assistant responses.
- Addition of line charts for price history using `st.line_chart()`.

### Model Parameters
- Speech synthesis via Google Text-to-Speech (`gTTS`) with default language set to English.
- Audio streaming buffer size tuned for minimal latency with `streamlit_webrtc`.
- API rate limit handling via caching and request throttling.

---

## 2. Demo Videos & GIFs

### Voice Interaction Demo
![Voice Interaction Demo](./assets/voice_interaction_demo.gif)
_A demo showcasing voice commands triggering stock price fetch and verbal feedback._

### Text Interaction Demo
![Text Interaction Demo](./assets/text_interaction_demo.gif)
_A demo showing text input for stock symbols, with real-time data retrieval and chart display._

### Full End-to-End Demo Video
[Watch Full Demo on YouTube](https://youtu.be/your-demo-video-link)

---

## 3. Future Improvements
- Add support for more APIs and enhanced NLP for conversational AI.
- Optimize voice assistant with custom wake word detection.
- Deploy the app with automated Docker setup and CI/CD pipelines.

---

*This documentation will be updated continuously with new features and demos.*

---

**Last updated:** 2025-05-29

