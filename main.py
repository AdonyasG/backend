import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

# Environment Variables (Set in Dockerfile)
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/login")
def login():
    """Redirect user to Spotify login"""
    url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=playlist-read-private playlist-modify-public"
    return RedirectResponse(url)

@app.get("/callback")
def callback(code: str):
    """Handle Spotify authentication callback"""
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    tokens = response.json()
    redirect_url = f"https://frontend-8fm6.onrender.com?access_token={tokens['access_token']}&refresh_token={tokens['refresh_token']}"
    return RedirectResponse(url=redirect_url)
    # return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}


@app.get("/playlists")
def get_playlists(token: str):
    """Get user playlists"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)

    if response.status_code != 200:
        print("Spotify API error:", response.status_code, response.text)  # Debugging
        raise HTTPException(status_code=response.status_code, detail=response.text)

    print("Successful response:", response.json())  # Debugging
    return response.json()
