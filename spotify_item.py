from abc import ABC, abstractmethod
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import api_credentials

class SpotifyItem(ABC):
    def __init__(self, api_dict):
        self.api_dict = api_dict
        self.spot_api = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=api_credentials.client_ID, client_secret= api_credentials.client_SECRET, redirect_uri=api_credentials.redirect_URI))
        self.id = None
        self.name = None
        self.creators = []
        self.popularity = 0
        self.duration = 0
        self.features = {
            'danceability' : 0,
            'energy' : 0,
            'speechiness' : 0,
            'acousticness' : 0,
            'instrumentalness' : 0,
            'liveness' : 0,
            'valence' : 0
        }
    
    @abstractmethod
    def get_info(self):
        pass
    
    # @abstractmethod
    def get_display_info(self):
        pass

    @abstractmethod
    def get_audio_features(self):
        pass