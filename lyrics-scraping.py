import dotenv
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials 
import numpy as np
import pandas as pd
from lyricsgenius import Genius
import re
from requests.exceptions import HTTPError, Timeout

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

INLOVE_LINK = 'https://open.spotify.com/playlist/6adbmqEp3RbfD1jeaH3kXx?si=28f4a06c12794fb7'
HEARTBROKEN_LINK = 'https://open.spotify.com/playlist/3c0Nv5CY6TIaRszlTZbUFk?si=10c2eeb434d94f9f'
NONROMANCE_LINK = 'https://open.spotify.com/playlist/2ONwEw1Rw8EQS1nWjDxlzQ?si=a38ded2c46dd4c9d'

links = [INLOVE_LINK, HEARTBROKEN_LINK, NONROMANCE_LINK]
mood = ['in love', 'heartbroken', 'non-romance']
csv = ['inlove.csv', 'heartbroken.csv', 'nonromance.csv']

token = os.getenv("GENIUS_TOKEN")
genius = Genius(token)

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

# get list of songs from album and search for lyrics for each song using song title and artist name
for i in range(len(links)):
    tracks = get_tracks(links[i])
    df = pd.DataFrame(tracks, columns=['title','artist'])
    df['mood'] = mood[i]
    df['lyrics'] = 'none'
    for j in range(len(df)):
        try: 
            song = genius.search_song(df.iloc[j, 0], df.iloc[j, 1])
            if song is None:
                lyrics = 'none'
            else:
                lyrics = song.lyrics
                lyrics = re.sub("[\(\[].*?[\)\]]", "", lyrics)
                lyrics = re.sub("\n", " ", lyrics)
                lyrics = lyrics[lyrics.find('Lyrics'):].replace('Lyrics ','')
            df.iloc[j, 3] = lyrics
        except HTTPError as e:
            print(e.errno)    # status code
            print(e.args[0])  # status code
            print(e.args[1])  # error message
        except Timeout:
            pass
    df.to_csv(csv[i], index=False)
    print('done', mood[i])

