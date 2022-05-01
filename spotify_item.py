from abc import ABC, abstractmethod
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyItem(ABC):
    """Represents a Song or Song Collection (Album, or Playlist)"""

    def __init__(self, api_dict):
        """
        SpotifyItem Constructor
        :param api_dict: A Dictionary from the API that holds all the details about a Spotify Item
        """
        self.api_dict = api_dict
        # Credentials are given after setting up a Spotify Developer account
        client_credentials_manager = SpotifyClientCredentials(client_id='4ac5a4f3e31640ec8025137207814eed',
                                                              client_secret='c5392ce82e0341ad95dc3b2450ec1549')
        self.spot_api = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.id = None
        self.name = None
        self.creators = []
        self.popularity = 0
        self.duration = 0
        self.features = {
            'danceability': 0,
            'energy': 0,
            'speechiness': 0,
            'acousticness': 0,
            'instrumentalness': 0,
            'liveness': 0,
            'valence': 0
        }
        self.cover_image = ''

    @abstractmethod
    def get_info(self):
        """
        Gets the details about a Spotify Item from the API
        """
        pass

    @abstractmethod
    def get_audio_features(self):
        """
        Gets the statistics about a Spotify Item from the API
        """
        pass
