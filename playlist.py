from song_collection import SongCollection
from song import Song


class Playlist(SongCollection):
    """Represents a Playlist"""

    def __init__(self, api_dict):
        """
        Playlist Constructor
        :param api_dict: A Dictionary from the API that holds all the details about a Playlist
        """
        super().__init__(api_dict)

    def get_info(self):
        # Assigns the Dictionary representing a Playlist from the Spotify API to a variable
        plist = self.api_dict
        # Gets all the necessary values from the Dictionary and stores them in their variables
        self.id = plist['id']
        self.name = plist['name']
        self.creators.append(plist['owner']['display_name'])
        self.num_songs = plist['tracks']['total']
        self.cover_image = plist['images'][0]['url']

    def get_audio_features(self):
        self.get_tracks()
        return super().get_audio_features()

    def get_tracks(self):
        """
        Adds Songs to the list of Songs 100 songs at a time
        """
        offset = 0
        buffer = 100
        remaining = self.num_songs
        while remaining > 0:
            # Gets a list of 100 Songs from the API in the form of a Dictionary
            plist_songs = self.spot_api.playlist_tracks(playlist_id=self.id, offset=offset, limit=buffer)
            # 'items' is a key that produces a list of all the Songs, each song is represented as a Dictionary
            # This loop iterates through that dictionary and adds the Song to the list
            for s in plist_songs['items']:
                song_dict = s['track']
                # If a Song is removed from Spotify that was once in a Playlist, it remains in the Playlist as None
                # This if makes sure no Songs are added to the list that do no exist (are None)
                if song_dict is not None and song_dict['id'] is not None:
                    song = Song(song_dict)
                    song.get_info()
                    self.songs.append(song)
                    self.popularity += song.popularity
                    self.duration += song.duration

            # Increases the starting index to grab the next 100 Songs
            offset += buffer
            remaining -= buffer
        self.popularity /= self.num_songs

    def __str__(self):
        return (f'Name: {self.name}\nCreator: {self.creators}\
        \nSongs: {self.num_songs}\nDuration: {self.duration}\nPopularity: {self.popularity}')
