from song_collection import SongCollection
from song import Song


class Album(SongCollection):
    """Represents an Album"""

    def __init__(self, api_dict):
        """
        Album Constructor
        :param api_dict: A Dictionary from the API that holds all the details about an Album
        """
        super().__init__(api_dict)

    def get_info(self):
        # Assigns the Dictionary representing a Album from the Spotify API to a variable
        albm = self.api_dict
        # Gets all the necessary values from the Dictionary and stores them in their variables
        self.id = albm['id']
        self.name = albm['name']
        self.num_songs = albm['total_tracks']
        self.cover_image = albm['images'][0]['url']
        for creator in albm['artists']:
            self.creators.append(creator['name'])

    def get_audio_features(self):
        self.get_tracks()
        return super().get_audio_features()

    def get_tracks(self):
        """
        Adds Songs to the list of Songs, 50 songs at a time
        """
        offset = 0
        buffer = 50
        remaining = self.num_songs
        while remaining > 0:
            # Gets 50 Songs from the API in the form of a Dictionary
            alb_songs = self.spot_api.album_tracks(album_id=self.id, offset=offset, limit=buffer)
            # Iterates through the Dictionary and adds Songs the list of Songs
            for s in alb_songs['items']:
                # Gets the details about a Song in the form of Dictionary
                s_dict = self.spot_api.track(s['id'])
                song = Song(s_dict)
                song.get_info()
                self.songs.append(song)
                self.popularity += song.popularity
                self.duration += song.duration
            # Increases the starting index by 50 to grab the next 50 Songs in the Album
            offset += buffer
            remaining -= buffer
        # Divides the total popularity by the number of songs to get the average
        self.popularity /= self.num_songs

    def __str__(self):
        return (f'Name: {self.name}\nCreator: {self.creators}\
        \nSongs: {self.num_songs}\nDuration: {self.duration}\nPopularity: {self.popularity}')
