from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
USERNAME = os.environ.get("USERNAME")
USER_ID = os.environ.get("USER_ID")

SPOTIPY_REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-public"

year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{year}"
billboard = requests.get(url=URL)

soup = BeautifulSoup(billboard.text, "html.parser")

songs = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")

playlist = [song.text for song in songs]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, redirect_uri=SPOTIPY_REDIRECT_URI))
playlist_url = sp.user_playlist_create(user=USERNAME, name=f"{year} Nostalgia Songs", description=f"{year} in Songs")
playlist_id = playlist_url["id"]

results = [sp.search(q=f"{song_name}", type="track") for song_name in playlist]

tracks = [x["tracks"]["items"][0]["external_urls"]["spotify"] for x in results]

sp.playlist_add_items(playlist_id=playlist_id, items=tracks)
print("Successfully Done Boss")
