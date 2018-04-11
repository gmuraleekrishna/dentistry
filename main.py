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

class Dentistry(tk.Frame):

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
    app = Dentistry()
    app.master.title("Dentistry")
    def on_close():
        if messagebox.askokcancel("Quit", "Closing the application will delete all the data. Do you want to quit?"):
            app.master.destroy()
    def about():
        messagebox.showinfo("About", "Author: Muraleekrishna Gopinathan [gmuraleekrishna@outlook.com], License: GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html")
    menubar = tk.Menu(app.master)
    menubar.add_command(label="About", command=about)
    menubar.add_command(label="Quit", command=on_close)

# display the menu
    app.master.config(menu=menubar)
    app.master.minsize(300, 300)
    
    app.master.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()
