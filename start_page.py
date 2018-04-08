# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from get_angle_page import GetAnglePage
from get_area_page import GetAreaPage
from generate_report_page import GenetateReportPage

LARGE_FONT= ("Verdana", 12)

class StartPage(tk.Frame):

    def __init__(self, parent, database):
        self.database = database
        self.parent = parent
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        ttk.Button(self, text="Calculate Angle", command=self.__show_angle_page).pack(pady = 10)

        ttk.Button(self, text="Calculate Area", command=self.__show_area_page).pack(pady = 10)

        tk.Button(self, text="Generate PDF Report", width=20, command=self.__show_report_page).pack(pady=10)

    def __show_area_page(self):
        self.lower()
        frame = GetAreaPage(parent=self.parent, database=self.database)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()
    
    def __show_angle_page(self):
        self.lower()
        frame = GetAnglePage(parent=self.parent, database=self.database)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()
    
    def __show_report_page(self):
        self.lower()
        frame = GenetateReportPage(parent=self.parent, database=self.database)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()
        