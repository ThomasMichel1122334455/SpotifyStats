import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from playlist import Playlist
from album import Album
from results_frame import ResultsFrame
from song import Song
from search_frame import SearchFrame

import tkinter as tk
from PIL import Image, ImageTk
import urllib.request


class Gui(tk.Tk):
    """Represents the GUI"""

    def __init__(self):
        """
        Initializes the Gui
        """
        super().__init__()
        # The main colors used in the program
        self.background_color = 'White'
        self.text_color_1 = 'Black'
        self.button_color = '#E4E4E4'
        self.create_window()

        # Tk variables that hold the value of the search box and the options menu
        self.search_type = tk.StringVar()
        self.search_item = tk.StringVar()

        # Markst the starting index of the results
        self.search_buffer = 0
        # How many results to get at a time
        self.search_per_page = 8

        # Initializes where the images will be stored so they appear correctly on the window
        self.logo = ImageTk.PhotoImage(Image.open('SpotifyLogo.png').resize((450, 135)))
        self.result_imgs = [None] * self.search_per_page

        self.current_frame = tk.Frame()
        self.load_frame(SearchFrame(self))

    def create_window(self):
        """
        Adds the desired features to the window
        """
        self.title('SpotifyStats')
        window_width = 1250
        window_height = 800
        self.resizable(True, True)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.config(bg=self.background_color)

    def home_btn(self, master):
        """
        Creates a button that when clicked returns to the searching frame (the home page)
        :param master: The frame that the button belongs to
        :return: tk.Button
        """
        btn = tk.Button(
            master,
            text="SEARCH AGAIN",
            command=lambda: self.load_frame(SearchFrame(self)),
            bg=self.button_color,
            relief=tk.FLAT,
            height=2
        )
        return btn

    def load_frame(self, frame):
        """
        Swaps the current frame with the given frame
        :param frame: The tk.Frame to be switched to
        """
        self.current_frame.pack_forget()
        self.current_frame = frame
        self.current_frame.pack()

    def search(self):
        """
        Uses the SpotifyAPI to search for the given entry and passes the results into the ResultsFrame
        """
        # Gives access to the Spotify API which has a search function
        client_credentials_manager = SpotifyClientCredentials(client_id='4ac5a4f3e31640ec8025137207814eed',
                                                              client_secret='c5392ce82e0341ad95dc3b2450ec1549')
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        # The name of the desired item
        name = str(self.search_item.get())
        # The type of item that is being searched for
        spotify_type = str(self.search_type.get())
        if spotify_type != '' and name != '':
            # Searches for the desired item using the Spotify API
            results = sp.search(q=name, limit=self.search_per_page, type=spotify_type, offset=self.search_buffer)
            results = results[spotify_type + 's']['items']

            # Creates the respective SpotifyItems given the search results
            if str(self.search_type.get()) == 'track':
                for i, item in enumerate(results):
                    results[i] = Song(item)
            elif str(self.search_type.get()) == 'album':
                for i, item in enumerate(results):
                    results[i] = Album(item)
            elif str(self.search_type.get()) == 'playlist':
                for i, item in enumerate(results):
                    results[i] = Playlist(item)
            self.load_frame(ResultsFrame(self, results))

    def get_cover_img(self, url, size):
        """
        Produces a tkinter friendly image from the given url
        :param url: The SpotifyAPI url that links to a cover image
        :param size: The side length of the square image
        :return: ImageTk
        """
        # Gets the image from the url and stores it in cover.png
        urllib.request.urlretrieve(url, "cover.png")
        # returns the cover as a ImageTk
        return ImageTk.PhotoImage(Image.open('cover.png').resize((size, size)))


p = Gui()
p.mainloop()
