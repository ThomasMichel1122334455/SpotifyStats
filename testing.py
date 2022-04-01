import spotipy
from spotipy.oauth2 import SpotifyOAuth
import api_credentials
from playlist import Playlist
from album import Album
from song import Song


print('[0] Song\n[1] Playlist\n[2] Album')
chs = ['track', 'playlist', 'album']
search_type = chs[int(input('What are you searching for: '))]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=api_credentials.client_ID, client_secret= api_credentials.client_SECRET, redirect_uri=api_credentials.redirect_URI))
item_name = input(f'Enter the {search_type} name: ')
results = sp.search(q=item_name, limit=5, type= search_type)
for i, search_t in enumerate(results[search_type+'s']['items']):
    print(i, search_t['name'])
    
playlist_index = int(input(f'\nEnter the {search_type} you want to play: '))
selected = results[search_type+'s']['items'][playlist_index]

if search_type == 'track':
    i = Song(selected)
elif search_type == 'playlist':
    i = Playlist(selected)
elif search_type == 'album':
    i = Album(selected)

i.get_info()
i.get_audio_features()
print(i, '\n')
for ke, va in i.features.items():
    print(f'{ke} : {va}')
