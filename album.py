from song import Song
from song_collection import SongCollection

class Album(SongCollection):

    def __init__(self, api_dict):
        super().__init__(api_dict)
    

    def get_info(self):
        albm = self.api_dict
        self.id = albm['id']
        self.name = albm['name']
        self.num_songs = albm['total_tracks']
        for creator in albm['artists']:
            self.creators.append(creator['name'])
        self.get_tracks()
        

    def get_tracks(self):
        offset = 0
        buffer = 50
        remaining = self.num_songs
        while remaining > 0:
            alb_songs = self.spot_api.album_tracks(album_id=self.id, offset=offset, limit=buffer)
            for s in alb_songs['items']:
                if s is not None:
                    s_dict = self.spot_api.track(s['id'])
                    song = Song(s_dict)
                    song.get_info()
                    self.songs.append(song)
                    self.popularity += song.popularity
                    self.duration += song.duration
            offset += buffer
            remaining -= buffer
        self.popularity /= self.num_songs

    def __str__(self):
        return f'Name: {self.name}\nCreator: {self.creators}\nSongs: {self.num_songs}\nDuration: {self.duration}\nPopularity: {self.popularity}'
