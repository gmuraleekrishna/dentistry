# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import os, errno
import time
from get_image_file_page import GetImageFilePage

LARGE_FONT= ("Verdana", 12)

class StartPage(tk.Frame):

    def __init__(self, parent, database):
        self.database = database
        self.parent = parent
        self.report_folder_name = ""
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Report folder name", font=LARGE_FONT).grid(column=2, row=2, pady=10)
        self.entry = ttk.Entry(self, width=5)
        self.entry.grid(column=2, row=3, stick='ew')

        ttk.Button(self, text="Area", width=20, command=self.__show_area_page).grid(pady = 10, column=2, row=10)
        
        ttk.Button(self, text="Angle", width=20, command=self.__show_angle_page).grid(pady = 10, column=2, row=12)


    def __show_area_page(self):
        if(self.report_folder_name == ''):
            if(self.entry.get() == ''):
                root_folder = 'Report'
            else:
                root_folder = self.entry.get()
            self.report_folder_name =  root_folder.replace(' ','_') + '_' + time.strftime('%Y-%m-%d%H%M%S')
            self.entry.destroy()
            ttk.Label(self, text=self.report_folder_name).grid(column=2, row=3, stick='ew')
            self.__create_project_folder()
        self.image_type = 'area'
        self.__show_get_image_page()

    def __create_project_folder(self):
        area_folder_name =  os.path.join(self.report_folder_name, 'area')
        angle_folder_name =  os.path.join(self.report_folder_name, 'angle')
        try:
            os.makedirs(area_folder_name)
            os.makedirs(angle_folder_name)
            self.database.add('root', self.report_folder_name)
            self.database.add('area_folder', area_folder_name)
            self.database.add('angle_folder', angle_folder_name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                    raise

    def __show_angle_page(self):
        self.image_type = 'angle'
        self.__show_get_image_page()

    def __show_get_image_page(self):
        self.lower()
        frame = GetImageFilePage(parent=self.parent, database=self.database, image_type=self.image_type)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()