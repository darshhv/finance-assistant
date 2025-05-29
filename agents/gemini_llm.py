# C:\Users\darshan\finance_assistant_project\agents\gemini_llm.py
import os
import httpx

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiClient:
    def __init__(self, api_key=GEMINI_API_KEY):
        self.api_key = api_key
        self.endpoint = "https://api.gemini.com/v1/llm/chat"

    async def generate(self, prompt: str):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        json_data = {
            "prompt": prompt,
            "max_tokens": 500,
            "temperature": 0.7,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.endpoint, headers=headers, json=json_data)
            resp.raise_for_status()
            data = resp.json()
            return data.get("choices", [{}])[0].get("text", "No response")
