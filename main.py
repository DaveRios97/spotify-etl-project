import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import uuid
import datetime
from sqlalchemy import Column, Integer, String, UUID, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

def check_if_valid_data(df: pd.DataFrame) -> bool:
    """
    Validate that: 
        - The data frame is not empty.
        - The id and spotify_id values are unique.
        - The data frame has no null values.
        - The extraction day is equal to the current day.
    
    Args:
        df (pd.DataFrame): DataFrame.
    
    Returns: 
        True:
            if all conditions are valid.
           
        False:
            if any condition is invalid. 
    """
    
    # No data
    if df.empty:
        print('No se recuperó ninguina canción, finalizando ejecución')
        return False
    
    # Verify the unique UUID and spotify_id
    if pd.Series(df['id']).is_unique and pd.Series(df['spotify_id']).is_unique:
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
            raise Exception('At least one of the returned song does not come from today.')
        
    return True

if __name__ == "__main__":
    
    # Reading .env variables   
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")


    # Extraction Stage
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
    )

    playlist_id = '37i9dQZEVXbOa2lmxNORXQ' # Id of the "Top 50:Colombia" playlist
    results = sp.playlist_tracks(playlist_id)

    songs_names = []
    spotify_ids = []
    artist_names = []
    day_of_list = []
    timestamps = []
    day_positions = list(range(1, len(results['items']) + 1))
    custom_ids = list(uuid.uuid4() for _ in range(len(results['items'])))
    
    for track in results['items']:
        songs_names.append(track['track']['name'])
        spotify_ids.append(track['track']['id'])
        artist_names.append(track['track']['artists'][0]['name'])
        day_of_list.append(track['added_at'])
        timestamps.append(track['added_at'][0:10])
            
    songs_dict = {
        'id': custom_ids,
        'spotify_id': spotify_ids,
        'position': day_positions,
        'name': songs_names,
        'artist_name': artist_names,
        'day': day_of_list,
        'timestamp': timestamps
    }
    
    songs_df = pd.DataFrame(
        songs_dict, 
        columns=['id', 'spotify_id', 'position', 'name', 'artist_name', 'day', 'timestamp']
    )
    
    
    #Validation (trnasform) Stage   
    stage2_is_valid = False
    try:
        stage2_is_valid = check_if_valid_data(songs_df)
        if stage2_is_valid:
            print('Available to continue with the Loading Stage')
            
    except Exception as err:
        print('An error has occurred in the transformation stage: ', err)
    
    
    # Loading Stage 
    #Engine
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    #Models
    Base = declarative_base()
    
    class Song(Base):
        """
        Class that defines Song Model
        
        Atributes:
            id (UUID): Custom id.
            spotify_id (String): spotify provided by Sppotify.
            position (Integer): Song position on the current day in th top list.
            name (String): Song name.
            artist_name (String): Song's first artist name (main artist of the song)
            day (DateTime): Day of the Top List
            timestamp (DateTime): Timestamp of the playlist's day
        """
               
        __tablename__ = 'songs'       
        id = Column(UUID, primary_key=True)
        spotify_id = Column(String(22), nullable=False)
        position = Column(Integer, nullable=False)
        name = Column(String(50), nullable=False)
        artist_name = Column(String(50), nullable=False)
        day = Column(DateTime, nullable=False)
        timestamp = Column(DateTime, nullable=False)
    
    Base.metadata.create_all(engine)
    
    if stage2_is_valid:      
        try:
            session.bulk_insert_mappings(Song, songs_df.to_dict(orient='records'))
            session.commit()
            
        except SQLAlchemyError as err:
            print('Error: ', err)
            
        finally:
            session.close()  