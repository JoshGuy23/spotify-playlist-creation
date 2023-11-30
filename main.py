import requests
import os
import spotipy
import pprint
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: \n")
year = date.split("-")[0]

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=billboard_url)
response.raise_for_status()
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

song_list = [song.getText().strip() for song in soup.select("ul li ul li h3")]
artist_list = [artist.getText().strip() for artist in soup.select("ul li ul li h3 + span")]

with open("client_data.txt") as file:
    client_data = file.readlines()

oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://example.com",
                     scope="playlist-modify-private")

with open(".cache") as file:
    user_token = eval(file.readline())["access_token"]

sp = spotipy.Spotify(user_token)
user_id = sp.current_user()["id"]

results_list = []
for song in song_list:
    search_query = f"track: {song} year: {year}"
    try:
        result = sp.search(q=search_query, limit=1)
    except Exception:
        print("Song not found.")
        pass
    else:
        results_list.append(result)

with open(file="results.txt", mode="w") as file:
    pp = pprint.PrettyPrinter(stream=file)
    pp.pprint(results_list)

# print(song_list)
# print(artist_list)
