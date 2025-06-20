
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import io

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route for health check
@app.get("/")
def root():
    return {"message": "Dikanna API is alive."}

# Environment variables
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# Voice streaming endpoint
@app.post("/speak")
async def speak(request: Request):
    body = await request.json()
    text = body.get("text", "Ndewo, Dikanna API is speaking.")

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream",
        headers={
            "xi-api-key": ELEVEN_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.75
            }
        },
    )

    audio_stream = io.BytesIO(response.content)
    return StreamingResponse(audio_stream, media_type="audio/mpeg")
