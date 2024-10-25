import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import uuid
import datetime
from sqlalchemy import Column, String, UUID, DateTime, create_engine, insert
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DB_USER = 'DB_USER'
DB_PASSWORD = 'DB_PASSWORD'
DB_HOST = 'DB_HOST'
DB_PORT = 'DB_PORT'
DB_NAME = 'DB_NAME'

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
            raise Exception('At least one of the returned song does not come from today.')
        
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

    songs_names = []
    artist_names = []
    day_of_list = []
    timestamps = []
    
    for track in results['items']:
        songs_names.append(track['track']['name'])
        artist_names.append(track['track']['artists'][0]['name'])
        day_of_list.append(track['added_at'])
        timestamps.append(track['added_at'][0:10])
            
    songs_dict = {
        'id': [uuid.uuid4() for _ in range(len(results['items']))],
        'name': songs_names,
        'artist_name': artist_names,
        'day_of_list': day_of_list,
        'timestamp': timestamps
    }
    
    songs_df = pd.DataFrame(songs_dict, columns=['id', 'name', 'artist_name', 'day_of_list', 'timestamp'])
    
    # Validation (trnasform) Stage
    try:
        if check_if_valid_data(songs_df):
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
        """ Song Class
        """
        
        __tablename__ = 'songs_temp'       
        id = Column(UUID, primary_key=True)
        name = Column(String(50), nullable=False)
        artist_name = Column(String(50), nullable=False)
        day_of_list = Column(DateTime, nullable=False)
        timestamp = Column(DateTime, nullable=False)
    
    Base.metadata.create_all(engine)
    
    # I convert the df in dict wtih objects
    songs_objects = [
        {
            'id': uuid.uuid4(),
            'name': name,
            'artist_name': artist_name,
            'day_of_list': day,
            'timestamp': timestamp
        }
        for name, artist_name, day, timestamp in zip(songs_names, artist_names, day_of_list, timestamps)
    ]
    
    try:
        session.bulk_insert_mappings(Song, songs_objects)
        session.commit()
    except SQLAlchemyError as err:
        print('Error: ', err)
    finally:
        session.close()  
    
    # Insert without model(Song) neither ORM 
    #songs_df.to_sql('songs', engine, index=False, if_exists='append')
    
    # try:
    #     insert_stmt = insert(Song).values(songs_dict)
    #     session.execute(insert_stmt)
    #     session.commit() 
    
    # except SQLAlchemyError as err:
    #     session.rollback()
    #     print('Ocurrio un error: ', err)
    # finally:
    #     session.close()