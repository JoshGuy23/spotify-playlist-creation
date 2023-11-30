import requests
import os
import spotipy
# import pprint # Defunct: used to get a better understanding of the Spotify search results.
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

# Get the client ID and Secret for the Spotify/Spotipy app
# If you want the environment variables, please contact the program's creator.
CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]

# Get the date from the user as well as the year.
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: \n")
year = date.split("-")[0]

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"

# Get the billboard website corresponding to the user-entered date
response = requests.get(url=billboard_url)
response.raise_for_status()
webpage = response.text

# Start the html parser
soup = BeautifulSoup(webpage, "html.parser")

# Get each song from the website
song_list = [song.getText().strip() for song in soup.select("ul li ul li h3")]

# Defunct: Used to get each song's artist. Artist names ultimately not used.
# artist_list = [artist.getText().strip() for artist in soup.select("ul li ul li h3 + span")]

# Defunct: attempt to get id and secret from a separate file while testing authorization.
# Ended up using environment variables.
# with open("client_data.txt") as file:
#     client_data = file.readlines()

# Start the Spotipy Authentication
oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://example.com",
                     scope="playlist-modify-private")

# If the current access token has expired, create a new one. Then get the access token.
try:
    with open(".cache") as file:
        user_token = eval(file.readline())["access_token"]
except spotipy.SpotifyException:
    oauth.get_cached_token()
    with open(".cache") as file:
        user_token = eval(file.readline())["access_token"]

# Set up Spotipy using the access token and get the user id.
sp = spotipy.Spotify(user_token)
user_id = sp.current_user()["id"]

# Get the search results from Spotify
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

# Defunct: Added pretty-printed search results from Spotify into output file to
# get a better look at the format of the search results.
# with open(file="results.txt", mode="w") as file:
#     pp = pprint.PrettyPrinter(stream=file)
#     pp.pprint(results_list)

# Create the playlist
playlist_name = f"{date} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = playlist["id"]

# Get the URIs of each song found.
track_ids = [song["tracks"]["items"][0]["uri"] for song in results_list]

# Add the songs to a playlist.
sp.playlist_add_items(playlist_id=playlist_id, items=track_ids)
print(f"Congratulations! You now have a brand new Spotify playlist called '{playlist_name}'! Go check it out!")

# Defunct: Testing how the list of songs from the website is formatted.
# print(song_list)
# print(artist_list)
