import tkinter as tk
from result import Result

class ResultsFrame(tk.Frame):
    """Represents the frame that holds the search results"""
    def __init__(self, master, results):
        """
        Initializes the ResultsFrame
        :param master: The window the frame belongs to
        :param results: The search results from searching
        """
        super().__init__(master=master, bg= master.background_color)
        header = tk.Label(self, bg= master.background_color, text= 'RESULTS', font= 'Gothic_A1 26 bold', fg= master.text_color_1)
        header.pack()

        # Creates Results for the given results and packs them to the frame
        for i, r in enumerate(results):
            res = Result(self, r, i)
            res.pack()
        
        # A frame that holds all the button options
        button_frame = tk.Frame(self, bg=master.background_color)

        # A button that goes to the previous results
        back_btn = tk.Button(
            button_frame,
            text="BACK", 
            command= lambda: self.prev_results(),
            bg= master.button_color,
            relief= tk.FLAT,
            height=2
        )
        # A button that goes to the next results
        next_btn = tk.Button(
            button_frame,
            text="NEXT", 
            command= lambda: self.next_results(),
            bg= master.button_color,
            relief= tk.FLAT,
            height=2
        )
        home_btn = master.home_btn(button_frame)
        back_btn.pack(padx=20, side=tk.LEFT)
        home_btn.pack(padx=20, side=tk.LEFT)
        next_btn.pack(padx=20, side=tk.LEFT)
        
        button_frame.pack()
    
    def next_results(self):
        """
        Shifts the buffer foward to the next results
        """
        if next:
            self.master.search_buffer += self.master.search_per_page
            self.master.search()
            

    def prev_results(self):
        """
        Shifts the buffer back to the previous results
        """
        if self.master.search_buffer != 0:
            self.master.search_buffer -= self.master.search_per_page
            self.master.search()
        