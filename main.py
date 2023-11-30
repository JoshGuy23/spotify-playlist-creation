import requests
from bs4 import BeautifulSoup

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: \n")

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=billboard_url)
response.raise_for_status()
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

song_list = [song.getText().strip() for song in soup.select("ul li ul li h3")]
artist_list = [artist.getText().strip() for artist in soup.select("ul li ul li h3 + span")]

print(song_list)
print(artist_list)

