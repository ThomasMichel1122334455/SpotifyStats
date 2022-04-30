from spotify_item import SpotifyItem

class SongCollection(SpotifyItem):
    """Represents an Album or Playlist"""

    def __init__(self, api_dict):
        """
        SongCollection Constructor
        
        :param api_dict: A Dictionary from the API that holds all of the details about a Spotify Item
        """
        super().__init__(api_dict)
        self.num_songs = 0
        self.songs = []
    
    
    def get_tracks(self):
        """
        Gets all the Songs in the Album or Playlist and adds it to the list of Songs
        """
        pass


    def get_audio_features(self):
        # A list of all the IDs of the Songs in the Album or Playlist
        song_ids = [song.id for song in self.songs]
        offset = 0
        buffer = 100
        remaining = self.num_songs
        while remaining > 0:
            # Using a Song's ID, this gets the features (stats) for the first 100 Songs in the form of a Dictionary from the Spotify API
            stats = self.spot_api.audio_features(song_ids[offset : offset+buffer])
            for song_stats in stats:
                if song_stats is not None:
                    # Adds the value of the feature to their respective key in the dictionary of features
                    for feat in self.features.keys():
                        self.features[feat] += song_stats[feat]
            # increases the starting point by 100 to search the next 100 songs
            offset += buffer
            remaining -= buffer
        
        # Divides the features by the number of songs in the Album or Playlist to get the average of the features
        for feat in self.features.keys():
            self.features[feat] /= self.num_songs
        self.features['popularity'] = self.popularity/100
