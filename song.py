from spotify_item import SpotifyItem

class Song(SpotifyItem):
    def __init__(self, api_dict):
        """
        Song Constructor
        :param api_dict: A Dictionary from the API that holds all of the details about a Spotify Item
        """
        super().__init__(api_dict)
        
    def get_info(self):
        # Assigns the Dictionary representing a Song from the Spotify API to a variable
        song = self.api_dict
        # Gets all the necesary values from the Dictionary and stores them in their variables
        self.id = song['id']
        self.name = song['name']
        self.popularity = song['popularity']
        self.duration = song['duration_ms']
        self.cover_image = song['album']['images'][0]['url']
        for creator in song['artists']:
            self.creators.append(creator['name'])
        # There are a few, rare, songs that are stored in Playlists that get removed from Spotify but remain as None in the Playlist so this expect cathes those cases
        # For this reason this except should not occur when searching for just a song or an album
          
    def get_audio_features(self):
        # Gets the features (stats) for a single song
        track_features = self.spot_api.audio_features(self.id)[0]
        # Some Songs are not given features by Spotify
        # This if makes sure the Song has features before going throught the values
        if track_features is not None:
            for feature in self.features.keys():
                self.features[feature] = track_features[feature]
        self.features['popularity'] = self.popularity/100
    
    def __str__(self):
        return f'Name: {self.name}\nAlbum: {self.album}\nArtists: {self.creators}\nPopularity: {self.popularity}'
