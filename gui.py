import spotipy
from spotipy.oauth2 import SpotifyOAuth
import api_credentials
from playlist import Playlist
from album import Album
from song import Song
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
from ctypes import windll



class Gui:

    def __init__(self):
        self.current_page = None
        self.window = None
        self.search_type = None
        self.search_item = None
        self.logo = None
        self.result_imgs = []
        self.search_buffer = 0
        self.search_per_page = 8

    
    def create_window(self):
        windll.shcore.SetProcessDpiAwareness(1)
        self.window = tk.Tk()
        self.window.title('SpotifyStats')
        window_width = 3000
        window_height = 1900
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
        self.result_imgs = [None] * self.search_per_page
        self.search_frame = self.create_search_frame()
        self.current_frame = self.search_frame
        self.current_frame.pack()
        self.window.mainloop()
    

    def create_search_frame(self):
        self.search_buffer = 0
        self.search_type = tk.StringVar()
        self.search_item = tk.StringVar()
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
        if tp != '' and nm != '':
            results = sp.search(q=nm, limit=self.search_per_page, type=tp, offset=self.search_buffer)
            results = results[tp+'s']['items']
            if str(self.search_type.get()) == 'track':
                for i, item in enumerate(results):
                    results[i] = Song(item)
            elif str(self.search_type.get()) == 'album':
                for i, item in enumerate(results):
                    results[i] = Album(item)
            elif str(self.search_type.get()) == 'playlist':
                for i, item in enumerate(results):
                    results[i] = Playlist(item)
            self.load_frame(self.create_results_frame(results))


    def create_results_frame(self, results):
        results_frame = tk.Frame(self.window, bg = 'White')
        header = tk.Label(results_frame, bg= 'white', text= 'RESULTS', font= 'Gothic_A1 26 bold')
        header.pack()
        for i, r in enumerate(results):
            res = self.create_result(i, results_frame, r)
            res.pack()
        button_frame = tk.Frame(results_frame, bg='White')
        back_btn = tk.Button(
            button_frame,
            text="BACK", 
            command= lambda: self.prev_results(),
            bg= '#E4E4E4',
            relief= tk.FLAT,
            height=2
        )
        next_btn = tk.Button(
            button_frame,
            text="NEXT", 
            command= lambda: self.next_results(),
            bg= '#E4E4E4',
            relief= tk.FLAT,
            height=2
        )
        search_again = tk.Button(
            button_frame,
            text="SEARCH AGAIN", 
            command= lambda: self.load_frame(self.create_search_frame()),
            bg= '#E4E4E4',
            relief= tk.FLAT,
            height=2
        )
        back_btn.pack(padx=40, side=tk.LEFT)
        search_again.pack(padx=40, side=tk.LEFT)
        next_btn.pack(padx=40, side=tk.LEFT)
        
        button_frame.pack()
        return results_frame


    def next_results(self):
        if next:
            self.search_buffer += self.search_per_page
            self.search()
            

    def prev_results(self):
        if self.search_buffer != 0:
            self.search_buffer -= self.search_per_page
            self.search()
            

    def create_result(self, index, master, result):
        width = 1500
        height = 200
        result_item = tk.Canvas(master, bg='white', bd=0, width= width, height=height)
        result.get_info()
        self.result_imgs[index] = self.get_cover_img(result.cover_image, 150)
        creator_names = ', '.join(result.creators)
        result_item.create_text((200, (height/2)-20), text=result.name, anchor=tk.W, font= 'Gothic_A1 12 bold')
        result_item.create_image(25, 25, image=self.result_imgs[index], anchor=tk.NW)
        result_item.create_text(
            (200, (height/2)+20), 
            text= creator_names,
            anchor=tk.W, 
            font= 'Gothic_A1 8 bold', 
            fill= 'grey')
        result_item.bind("<Button-1>", lambda event: self.load_frame(self.create_stats_frame(result)))
        return result_item

    
    def create_stats_frame(self, selected):
        stats_page = tk.Frame(self.window, bg='White')
        selected.get_audio_features()
        self.create_stats_header(stats_page, selected).pack()
        percent_frame = tk.Frame(stats_page, bg='White')
        percent_frame.pack()
        
        c = 0
        r = 0
        for ke, va in selected.features.items():
            if r == 4:
                r = 0
                c = 1
            stat_bar = self.create_percent_bar(percent_frame, ke, va)
            stat_bar.grid(column=c, row=r)
            r += 1
        home_btn = tk.Button(
            stats_page,
            text="SEARCH AGAIN", 
            command= lambda: self.load_frame(self.create_search_frame()),
            bg= '#E4E4E4',
            relief= tk.FLAT,
            height=2
        )
        home_btn.pack()
        return stats_page


    def create_percent_bar(self, master, title, percent):
        w = 1500
        h = 200
        header = f'{title.capitalize()}:  {(int(percent*100))}%'
        bar = tk.Canvas(
            master,
            width=w,
            height= h,
            bg='White',
            highlightthickness=0
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


    def create_stats_header(self, master, spotify_item):
        header = tk.Canvas(master, bg= "White", width=3000, height=800, highlightthickness=0)
        self.result_imgs[0] = self.get_cover_img(spotify_item.cover_image, 600)
        header.create_image(50, 100, image=self.result_imgs[0], anchor=tk.NW)
        header.create_text(
            700, 
            125,
            text=spotify_item.name,
            anchor=tk.NW, 
            font= 'Gothic_A1 30 bold', 
            fill= 'Black')
        creators = ', '.join(spotify_item.creators)
        header.create_text(
            700, 
            240,
            text=creators,
            anchor=tk.NW, 
            font= 'Gothic_A1 15 bold', 
            fill= 'Grey')
        time = self.duration_convert(spotify_item.duration)
        header.create_text(
            700, 
            310,
            text=time,
            anchor=tk.NW, 
            font= 'Gothic_A1 15 bold', 
            fill= 'Grey')
        return header


    def duration_convert(self, duration):
        time = {
            'Weeks' : 0,
            'Days' : 0,
            'Hours' : 0,
            'Minutes' : 0,
            'Seconds' : 0,
        }
        time['Seconds'] = duration//1000
        while time['Seconds'] > 60:
            if time['Seconds']//604800:
                time['Seconds'] -= 604800
                time['Weeks'] += 1
            elif time['Seconds']//86400:
                time['Seconds'] -= 86400
                time['Days'] += 1
            elif time['Seconds']//3600:
                time['Seconds'] -= 3600
                time['Hours'] += 1
            elif time['Seconds']//60:
                time['Seconds'] -= 60
                time['Minutes'] += 1
        duration = ''
        for tme, value in time.items():
            if value > 0:
                duration += f'{value} {tme} '
        return duration


    def get_cover_img(self, url, size):
        urllib.request.urlretrieve(url, "cover.png")
        return ImageTk.PhotoImage(Image.open('cover.png').resize((size, size)))


    def load_frame(self, frame):
        self.current_frame.pack_forget()
        self.current_frame = frame
        self.current_frame.pack()
            
run = Gui()
run.create_window()

