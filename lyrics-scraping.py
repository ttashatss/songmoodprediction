from tokenize import Token
import pandas as pd 
from lyricsgenius import Genius
import re
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GENIUS_TOKEN")
genius = Genius(token)

csv = ['inlove.csv', 'heartbroken.csv', 'nonromance.csv']

df = pd.concat(
    map(pd.read_csv, csv), ignore_index=True)

df['lyrics'] = 'None'

for i in range(len(df)):
    song = genius.search_song(df.iloc[i, 0], df.iloc[i, 1])
    if song is None:
        lyrics = 'none'
    else:
        lyrics = song.lyrics
        lyrics = re.sub("[\(\[].*?[\)\]]", "", lyrics)
        lyrics = re.sub("\n", " ", lyrics)
        lyrics = lyrics[lyrics.find('Lyrics'):].replace('Lyrics ','')
    df.iloc[i, 3] = lyrics

df.to_csv(r'lyrics.csv', index=False)