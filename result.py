import tkinter as tk
from stats_frame import StatsFrame

class Result(tk.Canvas):
    """Represents a single search result"""
    def __init__(self, frame, result, index):
        """
        Initializes the Result
        :param frame: The frame the Result belongs to
        :param result: The SpotifyItem the Result is representing
        :param index: The number result being displayed
        """
        width = 600
        height = 80
        super().__init__(master=frame, bg=frame.master.background_color, bd=0, width= width, height=height)
        
        # Gets the information about the given SpotifyItem
        result.get_info()
        # Adds the SpotifyItem's Image to the List of Images so it can properly load in the window
        frame.master.result_imgs[index] = frame.master.get_cover_img(result.cover_image, 60)
        creator_names = ', '.join(result.creators)
        # Adds the SpotifyItem's name to the Result Canvas
        self.create_text((80, (height/2)-10), text=result.name, anchor=tk.W, font= 'Gothic_A1 12 bold', fill=frame.master.text_color_1)
        # Adds the SpotifyItem's cover image to the Result Canvas
        self.create_image(10, 10, image=frame.master.result_imgs[index], anchor=tk.NW)
        # Adds the SpotifyItem's creators to the Result Canvas
        self.create_text(
            (80, (height/2)+10), 
            text= creator_names,
            anchor=tk.W, 
            font= 'Gothic_A1 8 bold', 
            fill= 'Grey')

        # Binding that changes the frame to the StatsFrame when a Result is left clicked on
        self.bind("<Button-1>", lambda event: frame.master.load_frame(StatsFrame(frame.master, result)))