from spotify_item import SpotifyItem

class Song(SpotifyItem):
    def __init__(self, api_dict):
        super().__init__(api_dict)
        self.album = None
        
    def get_info(self):
        try:
            song = self.api_dict
            self.id = song['id']
            self.name = song['name']
            self.popularity = song['popularity']
            self.duration = song['duration_ms']
            self.album = song['album']['name']
            self.creators = []
            for creator in song['artists']:
                self.creators.append(creator['name'])
        except TypeError:
            print('Couldn\'t read data from this song')
            
    def get_audio_features(self):
        track_features = self.spot_api.audio_features(self.id)[0]
        for feature in self.features.keys():
            self.features[feature] = track_features[feature]
    
    def __str__(self):
        return f'Name: {self.name}\nAlbum: {self.album}\nArtists: {self.creators}\nPopularity: {self.popularity}'