import matplotlib
matplotlib.use("TkAgg")

import tkinter as tk
from tkinter import ttk
import cv2

from start_page import StartPage
from get_area_page import GetAreaPage
from get_angle_page import GetAnglePage

LARGE_FONT= ("Verdana", 12)

class Dentistry(tk.Frame):

    def __init__(self, parent=None):
        
        tk.Frame.__init__(self, parent)
        self.pack()
        
        self.container = tk.Frame(self, width=200, height=200)
        self.container.pack_propagate(True)
        self.container.pack(side="top", fill="both", expand = True)

        frame = StartPage(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        

if __name__ == "__main__":
    app = Dentistry()
    app.master.title("Dentistry")
    app.master.minsize(300, 300)
    app.mainloop()
