import json
import math

import pandas as pd
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open('spotifykeys.json') as f:
    data = f.readlines()

spotifykeys = json.loads(''.join(data))


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotifykeys['client_id'],
                                                           client_secret=spotifykeys['client_secret'])

bearerToken=spotifykeys['bearerToken']


def search_and_get_id(artist, title):

    results=sp.search(q='{} {}'.format(artist, title), limit=1)
    try:
        return results['tracks']['items'][0]['id']
    except:
        print('UNABLE TO GET ID: {} - {}'.format(artist, title))


def set_liked_by_id(ids):
    headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(bearerToken),
        }
    return requests.put('https://api.spotify.com/v1/me/tracks?ids={}'.format(','.join(ids)), headers=headers)


def set_liked_wrapper(ids):
    """ request can only be for a max of 50 ids so this will call multiple times"""
    maxIds=50
    totalIds=len(ids)
    totalRequests=math.ceil(totalIds / maxIds)
    for n in range(totalRequests):
        startIdx=n * maxIds
        if n < totalRequests:
            endIdx=startIdx + maxIds
        else:
            endIdx=None
        response=set_liked_by_id(ids[startIdx:endIdx])
        print(response, response.text)


df=pd.read_csv('youtube_liked_songs.csv')

songs=df.to_dict(orient='list')
artists=songs['artist']
titles=songs['title']
song_ids=[]
for i, artist in enumerate(artists):
    title=titles[i]
    _id=search_and_get_id(artist, title)
    if type(_id) == str:
        song_ids.append(_id)

response=set_liked_wrapper(song_ids[100:])
