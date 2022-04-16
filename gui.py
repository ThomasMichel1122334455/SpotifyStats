import tkinter as tk
import ctypes
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import api_credentials
from playlist import Playlist
from album import Album
from song import Song
import urllib.request
from PIL import Image, ImageTk

import urllib.request

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Gui:

    def __init__(self):
        self.current_page = None
        self.window = None
        self.search_page = None
        self.search_type = None
        self.search_item = None
        self.results_page = None
        self.stats_page = None
        self.logo = None
        self.result_imgs = []

    
    def create_window(self):
        self.window = tk.Tk()
        self.window.title('SpotifyStats')
        window_width = 3000
        window_height = 1600
        self.window.resizable(True, True)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y= int(screen_height/2 - window_height/2)
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.window.iconbitmap('./spotify.ico')
        self.window.config(bg='White')
        self.search_type = tk.StringVar()
        self.search_item = tk.StringVar()
        self.logo = tk.PhotoImage(file='SpotifyLogo.png')
        self.result_imgs = [None] * 8
        self.search_frame = self.create_search_frame()
        self.current_frame = self.search_frame
        self.current_frame.pack()
        self.window.mainloop()
    
    def create_search_frame(self):
        search_frame = tk.Frame(bg = 'White')
        
        logo_header = tk.Frame(
            search_frame,
            bg='White')

        search_bar = tk.Frame(
            search_frame,
            bg='White',
            height=50
        )

        search_entry = tk.Entry(
            search_bar,
            bg='#F5F5F5',
            relief=tk.FLAT,
            font= 'Gothic_A1 20',
            width=30,
            textvariable=self.search_item
        )

        search_btn = tk.Button(
            search_bar,
            text="SEARCH", 
            command= self.search,
            bg= '#E4E4E4',
            relief= tk.FLAT,
            height=2
        )

        spotify_logo = tk.Label(
            logo_header,
            image= self.logo,
            bg='White'
        )

        spotify_stats = tk.Label(
            logo_header,
            text= 'Stats',
            font= 'Gothic_A1 63 bold',
            bg = 'White'
        )

        menu_btn = tk.Menubutton(
            search_frame,
            bg = '#E4E4E4',
            text= 'Searching For'
        )

        options_menu = tk.Menu(
            menu_btn,
            tearoff= 0,
        )

        options_menu.add_radiobutton(label='Song', value='track', variable= self.search_type)
        options_menu.add_radiobutton(label='Album', value='album', variable= self.search_type)
        options_menu.add_radiobutton(label='Playlist', value='playlist', variable= self.search_type)
        menu_btn['menu'] = options_menu

        spotify_logo.pack(padx = 5, pady = 5, side=tk.LEFT)
        spotify_stats.pack(padx = 5, pady = 5, side=tk.LEFT)

        search_entry.pack(padx = 0, pady = 5, side=tk.LEFT, fill=tk.BOTH)
        search_btn.pack(padx = 0, pady = 5, side=tk.LEFT, fill=tk.BOTH)

        logo_header.pack(padx=5, pady=250)
        search_bar.pack(padx=5, pady= 25)
        menu_btn.pack(padx=5, pady= 25)

        return search_frame

    def search(self):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=api_credentials.client_ID, client_secret= api_credentials.client_SECRET, redirect_uri=api_credentials.redirect_URI))
        nm = str(self.search_item.get())
        tp = str(self.search_type.get())
        results = sp.search(q=nm, limit=8, type= tp)
        results = results[tp+'s']['items']
        self.load_frame(self.create_results_frame(results))

    def create_results_frame(self, results):
        results_frame = tk.Frame(self.window, bg = 'White')
        header = tk.Label(results_frame, bg= 'white', text= 'Results', font= 'Gothic_A1 30 bold')
        header.pack()
        for i, r in enumerate(results):
            res = self.create_result(i, results_frame, r)
            res.pack()
        return results_frame
    
    def create_result(self, index, master, result):
        width = 1500
        height = 200
        result_item = tk.Canvas(master, bg='white', bd=0, width= width, height=height)
        # img = self.cover_img
        # result_item.create_rectangle(50, height/4, 150, height*(3/4), fill='Green')
        result_item.create_text((200, (height/2)-20), text=result['name'], anchor=tk.W, font= 'Gothic_A1 12 bold')
        if str(self.search_type.get()) == 'playlist':
            creator_names = result['owner']['display_name']
            self.result_imgs[index] = self.get_cover_img(result['images'][0]['url'], 150)
        elif str(self.search_type.get()) == 'track':
            creator_names = ', '.join([artist['name'] for artist in result['artists']])
            self.result_imgs[index] = self.get_cover_img(result['album']['images'][0]['url'], 150)
        else:
            creator_names = ', '.join([artist['name'] for artist in result['artists']])
            self.result_imgs[index] = self.get_cover_img(result['images'][0]['url'], 150)
        result_item.create_image(25, 25, image=self.result_imgs[index], anchor=tk.NW)
        result_item.create_text(
            (200, (height/2)+20), 
            text= creator_names,
            anchor=tk.W, 
            font= 'Gothic_A1 8 bold', 
            fill= 'grey')
        result_item.bind("<Button-1>", lambda event: self.load_frame(self.create_stats_page(result)))
        return result_item

    def get_cover_img(self, url, size):
        urllib.request.urlretrieve(url, "cover.png")
        img = ImageTk.PhotoImage(Image.open('cover.png').resize((size, size)))
        return img

    def load_frame(self, frame):
        self.current_frame.pack_forget()
        self.current_frame = frame
        self.current_frame.pack()

    def create_stats_page(self, selected):
        stats_page = tk.Frame(self.window, bg='White')
        
        if str(self.search_type.get()) == 'track':
            i = Song(selected)
        elif str(self.search_type.get()) == 'playlist':
            i = Playlist(selected)
        elif str(self.search_type.get()) == 'album':
            i = Album(selected)

        i.get_info()
        i.get_audio_features()
        print(i, '\n')
        c = 0
        r = 0
        for ke, va in i.features.items():
            if r == 4:
                r = 0
                c = 1
            stat_bar = self.create_percent_bar(stats_page, ke, va)
            stat_bar.grid(column=c, row=r)
            r += 1
            print(f'{ke} : {va}')
        return stats_page

    def create_percent_bar(self, master, title, percent):
        w = 1500
        h = 200
        header = f'{title.capitalize()}:  {(int(percent*100))}%'
        bar = tk.Canvas(
            master,
            width=w,
            height= h,
            bg='White'
        )
        bar.create_text(
            50, 
            (h/2) - 25,
            text=header,
            anchor=tk.SW, 
            font= 'Gothic_A1 10 bold', 
            fill= 'grey')
        bar_width = 1000
        bar_height = 50
        bar.create_rectangle(50, (h/2), 50 + bar_width,(h/2) + bar_height, fill='#E4E4E4')
        bar.create_rectangle(50, (h/2), 50 + int(percent * bar_width), (h/2) + bar_height, fill='#1ED760')
        return bar

run = Gui()
run.create_window()
