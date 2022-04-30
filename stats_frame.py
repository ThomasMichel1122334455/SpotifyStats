import tkinter as tk
from percentage_bar import PercentageBar

class StatsFrame(tk.Frame):
    """Represents the frame that holds all the stats"""
    def __init__(self, master, selected):
        """
        Initializes the StatsFrame
        :param master: The window the frame belongs to
        :param selected: The SpotifyItem the user selected in the ResultsFrame
        """
        super().__init__(master, bg=master.background_color)
        
        # Gets the Stats for the selected SpotifyItem
        selected.get_audio_features()
        header = tk.Canvas(self, bg= master.background_color, width=1000, height=300, highlightthickness=0)
        # Adds the selected SpotifyItem cover image to the List
        master.result_imgs[0] = master.get_cover_img(selected.cover_image, 250)
        # Adds the image to the frame
        header.create_image(25, 25, image=master.result_imgs[0], anchor=tk.NW)
        # Adds the SpotifyItem name to the frame
        header.create_text(
            300, 
            60,
            text=selected.name,
            anchor=tk.NW, 
            font= 'Gothic_A1 20 bold',
            fill= master.text_color_1)
        creators = ', '.join(selected.creators)
        # Adds the SpotifyItem creators to the frame
        header.create_text(
            300, 
            92,
            text=creators,
            anchor=tk.NW, 
            font= 'Gothic_A1 15 bold', 
            fill= 'Grey')
        time = self.duration_convert(selected.duration)
        # Adds the SpotifyItem duration to the frame
        header.create_text(
            300, 
            120,
            text=time,
            anchor=tk.NW, 
            font= 'Gothic_A1 15 bold', 
            fill= 'Grey')
        header.pack()
        percent_frame = tk.Frame(self, bg=master.background_color)
        percent_frame.pack()
        
        c = 0
        r = 0
        # Adds the given stats in the form of percentage bars to the frame in grid a format
        for stat, value in selected.features.items():
            if r == 4:
                r = 0
                c = 1
            stat_bar = PercentageBar(master, percent_frame, stat, value)
            stat_bar.grid(column=c, row=r)
            r += 1
        master.home_btn(self).pack()

    
    def duration_convert(self, duration):
        """
        Converts milliseconds to a String of Weeks, Days, Hours, Minutes, and Seconds
        :param duration: The length of the SpotifyItem in milliseconds
        :return: String
        """
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
                amnt = time['Seconds']//604800
                time['Seconds'] -= 604800 * amnt
                time['Weeks'] += amnt
            elif time['Seconds']//86400:
                amnt = time['Seconds']//86400
                time['Seconds'] -= 86400 * amnt
                time['Days'] += amnt
            elif time['Seconds']//3600:
                amnt = time['Seconds']//3600
                time['Seconds'] -= 3600 * amnt
                time['Hours'] += amnt
            elif time['Seconds']//60:
                amnt = time['Seconds']//60
                time['Seconds'] -= 60 * amnt
                time['Minutes'] += amnt
        duration = ''
        # Returns the time information in the dictionary in the form of a String
        for tme, value in time.items():
            if value > 0:
                duration += f'{value} {tme} '
        return duration
