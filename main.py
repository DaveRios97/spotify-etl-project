import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Utils import write_file_utils
from datetime import datetime

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
)

playlist_id = '37i9dQZEVXbOa2lmxNORXQ' # Id de la playlist "Top 50:Colombia"
results = sp.playlist_tracks(playlist_id)
items = results['items']

tracks = []
songs = []
artists = []
artist_song = []
albums = []

for item in items:
    track = {}
    track['id'] = item['track']['id']
    track['added_at'] = item['added_at']
    track['name'] = item['track']['name']
    track['popularity'] = item['track']['popularity']
    track['artists'] = item['track']['artists']
    track['album'] = item['track']['album']
    tracks.append(track) 

for song in tracks:
    #Llenado de Songs  
    song_item = {}
    song_item['id'] = song['id']
    song_item['added_at'] = song['added_at']
    song_item['name'] = song['name']
    song_item['popularity'] = song['popularity']
    song_item['album_id'] = song['album']['id']
    song_item['album'] = song['album']['name']
    songs.append(song_item)
    
    #Llenado de albums
    album_item = {}
    album_item['id'] = song['album']['id']
    album_item['href'] = song['album']['href']
    album_item['images'] = song['album']['images']
    album_item['name'] = song['album']['name']
    album_item['release_date'] = song['album']['release_date']
    album_item['total_tracks'] = song['album']['total_tracks']
    albums.append(album_item)  
       
    for artist in song['artists']:
        
        #Llenaod de artistas
        artist_item = {}
        #Arreglar los duplicados
        if artist['id'] not in artists:
            artist_item['id'] = artist['id']
            artist_item['name'] = artist['name']
        artists.append(artist_item)
        
        #Llenado de artistas_canciones
        artist_song_item = {}
        artist_song_item['artist_id'] = artist['id']
        artist_song_item['artist_name'] = artist['name']
        artist_song_item['song_id'] = song['id']
        artist_song_item['song_name'] = song['name']
        artist_song.append(artist_song_item)
    
time = datetime.now()
songs_csv_name = f'songs-{time}'
artists_csv_name = f'artists-{time}'
artists_songs_csv_name = f'artist-songs-{time}'
json_name = f'top-50-{time}'


write_file_utils.write_csv(songs_csv_name, songs[0].keys(), songs)
write_file_utils.write_csv(artists_csv_name, artists[0].keys(), artists)
write_file_utils.write_csv(artists_songs_csv_name, artist_song[0].keys(), artist_song)
write_file_utils.write_json(json_name, items)


    
"""
Por Hacer

- Organizar mejor la extracción, para la generación de datos
- Terminar de generar los datos para guardarlos en tablas, en principio voy a exportarlas en CSV
- Integrar SQLAlchemy, crear los modelos y persistir en base de datos

"""











