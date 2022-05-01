import tkinter as tk


class PercentageBar(tk.Canvas):
    """Represents a percentage bar to display stats"""
    def __init__(self, master, frame, title, percent):
        """
        Initializes the PercentageBar
        :param master: The window the percentage bar frame belongs to
        :param frame: The frame the percentage bar belongs to
        :param title: The name of the stat being represented
        :param percent: The value of the stat being represented
        """
        super().__init__(master=frame)
        w = 500
        h = 75
        header = f'{title.capitalize()}:  {(int(percent*100))}%'
        self.config(
            width=w,
            height=h,
            bg=master.background_color,
            highlightthickness=0
        )
        # Adds the text of what stat the percentage bar represents over the bar
        self.create_text(
            25,
            (h/2) - 10,
            text=header,
            anchor=tk.SW,
            font='Gothic_A1 10 bold',
            fill='grey')
        bar_width = 350
        bar_height = 20
        # Create a rectangle that represents the background of the percentage bar
        self.create_rectangle(25, (h/2), 25 + bar_width, (h/2) + bar_height, fill='#abf3c5', outline='')
        # An identical rectanlge who's length is the length of the previous bar * the percent of the given stat
        self.create_rectangle(25, (h/2), 25 + int(percent * bar_width), (h/2) + bar_height, fill='#1ED760', outline='')
