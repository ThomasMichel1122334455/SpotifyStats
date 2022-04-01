from spotify_item import SpotifyItem

class SongCollection(SpotifyItem):

    def __init__(self, api_dict):
        super().__init__(api_dict)
        self.num_songs = 0
        self.songs = []
    
    def get_audio_features(self):
        song_ids = [song.id for song in self.songs]
        offset = 0
        buffer = 100
        remaining = self.num_songs
        while remaining > 0:
            features = self.spot_api.audio_features(song_ids[offset : offset+buffer])
            for i, songs in enumerate(features):
                try:
                    for feat in self.features.keys():
                        self.features[feat] += songs[feat]
                except TypeError:
                    print(f'Couldn\'t read data from song {offset+i+1}')
            offset += buffer
            remaining -= buffer
            
        for feat in self.features.keys():
            self.features[feat] /= self.num_songs
