import tkinter as tk
from tkinter import ttk

from get_angle_page import GetAnglePage
from get_area_page import GetAreaPage

LARGE_FONT= ("Verdana", 12)

class StartPage(tk.Frame):

    def __init__(self, parent, controller, database):
        self.controller = controller
        self.database = database
        self.parent = parent
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        ttk.Button(self, text="Calc Angle", command=self.__show_angle_page).pack()

        ttk.Button(self, text="Calc Area", command=self.__show_area_page).pack()

    def __show_area_page(self):
        self.lower()
        frame = GetAreaPage(parent=self.parent, controller=self, database=self.database)
        frame.grid(row=0,column=0,sticky="nsew")
        frame.lift()
    
    def __show_angle_page(self):
        self.lower()
        frame = GetAnglePage(parent=self.parent, controller=self, database=self.database)
        frame.grid(row=0,column=0,sticky="nsew")
        frame.lift()