import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from tkinter import ttk

from get_angle_page import GetAnglePage
from get_area_page import GetAreaPage

LARGE_FONT= ("Verdana", 12)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Get Angle",
                            command=lambda: controller.show_frame(GetAnglePage))
        button.pack()

        # button2 = ttk.Button(self, text="Get Area",
        #                     command=lambda: controller.show_frame(GetAreaPage))
        # button2.pack()