import tkinter as tk


class SearchFrame(tk.Frame):
    """Reprents the frame where people search for SpotifyItems"""

    def __init__(self, master):
        """
        Initializes the SearchFrame
        :param master: the window it belongs to
        """
        super().__init__(master=master, bg=master.background_color)

        # Resets the search box, options menu, and starting result index variables to their defaults
        master.search_buffer = 0
        master.search_type = tk.StringVar()
        master.search_item = tk.StringVar()

        # Frame that holds the Title of the App
        logo_header = tk.Frame(
            self,
            bg=master.background_color)

        # Frame that holds the search bar and button
        search_bar = tk.Frame(
            self,
            bg=master.background_color,
            height=50
        )

        # The search box
        search_entry = tk.Entry(
            search_bar,
            bg='#F5F5F5',
            relief=tk.FLAT,
            font='Gothic_A1 20',
            width=30,
            textvariable=master.search_item
        )

        # The search button
        search_btn = tk.Button(
            search_bar,
            text="SEARCH",
            command=master.search,
            bg=master.button_color,
            relief=tk.FLAT,
            height=2
        )

        # The Spotify logo
        spotify_logo = tk.Label(
            logo_header,
            image=master.logo,
            bg=master.background_color
        )

        # The "Stats" part of the title
        spotify_stats = tk.Label(
            logo_header,
            text='Stats',
            font='Gothic_A1 63 bold',
            fg=master.text_color_1,
            bg=master.background_color
        )

        # The options menu
        menu_btn = tk.Menubutton(
            self,
            bg=master.button_color,
            text='Searching For'
        )

        options_menu = tk.Menu(
            menu_btn,
            tearoff=0,
        )

        # Adds all the options to the options menu
        options_menu.add_radiobutton(label='Song', value='track', variable=master.search_type)
        options_menu.add_radiobutton(label='Album', value='album', variable=master.search_type)
        options_menu.add_radiobutton(label='Playlist', value='playlist', variable=master.search_type)
        menu_btn.config(menu=options_menu)

        spotify_logo.pack(padx=5, pady=5, side=tk.LEFT)
        spotify_stats.pack(padx=5, pady=5, side=tk.LEFT)

        search_entry.pack(padx=0, pady=5, side=tk.LEFT, fill=tk.BOTH)
        search_btn.pack(padx=0, pady=5, side=tk.LEFT, fill=tk.BOTH)

        logo_header.pack(padx=5, pady=50)
        search_bar.pack(padx=5, pady=25)
        menu_btn.pack(padx=5, pady=25)
