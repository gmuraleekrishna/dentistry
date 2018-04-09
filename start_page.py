# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from get_image_file_page import GetImageFilePage

LARGE_FONT= ("Verdana", 12)

class StartPage(tk.Frame):

    def __init__(self, parent, database):
        self.database = database
        self.parent = parent
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        ttk.Button(self, text="Calculate Angle", width=20, command=self.__show_angle_page).pack(pady = 10)

        ttk.Button(self, text="Calculate Area", width=20, command=self.__show_area_page).pack(pady = 10)

    def __show_area_page(self):
        self.image_type = 'area'
        self.__show_get_image_page()

    def __show_angle_page(self):
        self.image_type = 'angle'
        self.__show_get_image_page()

    def __show_get_image_page(self):
        self.lower()
        frame = GetImageFilePage(parent=self.parent, database=self.database, image_type=self.image_type)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()