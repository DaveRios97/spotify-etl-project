import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import uuid
import datetime

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def check_if_valid_data(df: pd.DataFrame) -> bool:
    
    # No data
    if df.empty:
        print('No se recuperó ninguina canción, finalizando ejecución')
        return False
    
    # Verify the UUID
    if pd.Series(df['id']).is_unique:
        pass
    else: 
        raise Exception('Primary key check is violated')
    
    # Check for null
    if df.isnull().values.any():
        raise Exception('Null value found')
    
    # Check that all timestamps are of today's date
    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    
    timestamps = df['timestamp'].to_list()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != today:
            raise Exception('At least one of the returned song does not come from today')
        
    return True

if __name__ == "__main__":

    # Extraction Stage
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
    )

    playlist_id = '37i9dQZEVXbOa2lmxNORXQ' # Id de la playlist "Top 50:Colombia"
    results = sp.playlist_tracks(playlist_id)

    songs_name = []
    artist_names = []
    day_of_list = []
    timestamps = []
    
    for track in results['items']:
        songs_name.append(track['track']['name'])
        artist_names.append(track['track']['artists'][0]['name'])
        day_of_list.append(track['added_at'])
        timestamps.append(track['added_at'][0:10])
            
    songs_dict = {
        'id': [uuid.uuid4() for _ in range(len(results['items']))],
        'songs_name': songs_name,
        'artist_name': artist_names,
        'day_of_list': day_of_list,
        'timestamp': timestamps,
    }
    
    songs_df = pd.DataFrame(songs_dict, columns=['id', 'songs_name', 'artist_name', 'day_of_list', 'timestamp'])
    
    # Validation (trnasform) Stage
    if check_if_valid_data(songs_df):
        print('Available to continue with the Loading Stage')