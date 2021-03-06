# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use("TkAgg")

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2

from database import Database
from start_page import StartPage
from get_area_page import GetAreaPage
from get_angle_page import GetAnglePage


LARGE_FONT= ("Verdana", 12)

class DentReckoner(tk.Frame):

    def __init__(self, parent=None):
        database = Database()
        tk.Frame.__init__(self, parent)
        self.pack()
        
        
        self.container = tk.Frame(self, width=200, height=200)
        self.container.pack_propagate(True)
        self.container.pack(side="top", fill="both", expand = True)

        frame = StartPage(parent=self.container, database=database)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        

if __name__ == "__main__":
    app = DentReckoner()
    app.master.title("Dent-Reckoner")
    def on_close():
        if messagebox.askokcancel("Quit", "Closing the application will delete all the data. Do you want to quit?"):
            app.master.destroy()

# display the menu
    app.master.minsize(300, 300)
    app.master.maxsize(600, 600)
    app.master.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()
