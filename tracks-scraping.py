import dotenv
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials 
import numpy as np
import pandas as pd

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

INLOVE_LINK = 'https://open.spotify.com/playlist/6adbmqEp3RbfD1jeaH3kXx?si=28f4a06c12794fb7'
HEARTBROKEN_LINK = 'https://open.spotify.com/playlist/3c0Nv5CY6TIaRszlTZbUFk?si=10c2eeb434d94f9f'
NONROMANCE_LINK = 'https://open.spotify.com/playlist/2ONwEw1Rw8EQS1nWjDxlzQ?si=a38ded2c46dd4c9d'

links = [INLOVE_LINK, HEARTBROKEN_LINK, NONROMANCE_LINK]
mood = ['in love', 'heartbroken', 'non-romance']
csv = ['inlove.csv', 'heartbroken.csv', 'nonromance.csv']

CLIENT_CREDENTIALS_MANAGER = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
SP = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)

# separate playlist uri from full url
def get_playlist_uri(playlist_link):
    return playlist_link.split("/")[-1].split("?")[0]

# get tracks in the playlist
def get_tracks(playlist_link):
    tracks = []
    playlist_uri = get_playlist_uri(playlist_link)
    for track in SP.playlist_tracks(playlist_uri)["items"]:
        #track_uri = track["track"]["uri"]
        track_name = track["track"]["name"]
        artist_name = track["track"]["artists"][0]["name"]
        result = track_name,artist_name #, SP.audio_features(track_uri)
        tracks.append(result)

    return tracks

for i in range(len(links)):
    tracks = get_tracks(links[i])
    df = pd.DataFrame(tracks, columns=['title','artist'])
    df['mood'] = mood[i]
    df.to_csv(csv[i], index=False)
    print('done', mood[i])

