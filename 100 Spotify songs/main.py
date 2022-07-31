import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input('what year you would like to travel to in YYY-MM-DD format:\n')
URL = f'https://www.billboard.com/charts/hot-100/{date}/'
response = requests.get(url=URL)
web_data = response.text
soup = BeautifulSoup(web_data, 'html.parser')
title_tag = soup.select(selector='li h3', id='title-of-a-story')
song_title = [title.text.strip() for title in title_tag]
# print(song_title)

# Create a Spotify API Client
SPOTIPY_CLIENT_ID = 'ada31cc0492947c3baee57d24a93bc1a'
SPOTIPY_CLIENT_SECRET = 'a7ae66e7cebe4ac5b1b707ecc302a716'
SPOTIPY_REDIRECT_URI = 'https://top-100-billboards/redirect'
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,  # Must be identical to the URI you entered in your Spotify Dashboard app
        scope="playlist-modify-private playlist-read-private user-read-recently-played",
        show_dialog=True,
        cache_path="token.txt",  # optional
    )
)
year = date.split("-")[0]
song_uris = []
# Get the current user dictionary
user = sp.current_user()
print(user)
user_id = user["id"]
print(user_id)
for song in song_title:
    track_info = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
    print(track_info)
    try:
        uri = track_info["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(len(song_uris))

# # creating a user's playlist
playlist = sp.user_playlist_create(user=user_id, description="Using BeautifulSoup we scrape the Top 100 Songs from "
                                                             "The Hot 100 - Billboard ", name=f"{date} Billboard "
                                                                                              f"100", public=False)
# print(playlist)
# # add songs to new playlist
add_songs = sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
c_user = sp.current_user_recently_played()
print(c_user)


