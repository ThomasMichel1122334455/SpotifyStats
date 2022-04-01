from song_collection import SongCollection
from song import Song

class Playlist(SongCollection):
    
    def __init__(self, api_dict):
        super().__init__(api_dict)


    def get_info(self):
        plist = self.api_dict
        self.id = plist['id']
        self.name = plist['name']
        self.creators.append(plist['owner']['display_name'])
        self.num_songs = plist['tracks']['total']
        self.get_tracks()


    def get_tracks(self):
        offset = 0
        buffer = 100
        remaining = self.num_songs
        while remaining > 0:
            plist_songs = self.spot_api.playlist_tracks(playlist_id=self.id, offset=offset, limit=buffer)
            for s in plist_songs['items']:
                song_dict = s['track']
                if song_dict is not None:
                    song = Song(song_dict)
                    song.get_info()
                    self.songs.append(song)
                    self.popularity += song.popularity
                    self.duration += song.duration
            offset += buffer
            remaining -= buffer
        self.popularity /= self.num_songs

    def __str__(self):
        return f'Name: {self.name}\nCreator: {self.creators}\nSongs: {self.num_songs}\nDuration: {self.duration}\nPopularity: {self.popularity}'

