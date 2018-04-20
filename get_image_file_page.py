from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import time
import os
from tkinter import messagebox

LARGE_FONT= ("Verdana", 12)
from get_angle_page import GetAnglePage
from get_area_page import GetAreaPage
from generate_report_page import GenetateReportPage

class GetImageFilePage(tk.Frame):

    def __init__(self, parent, database, image_type):
        self.parent = parent
        self.database = database
        self.image_type = image_type

        tk.Frame.__init__(self, self.parent, width=100, height=100)
        tk.Label(self, text="Calculate " + image_type.capitalize(), font=LARGE_FONT).grid(column=2, row=0, columnspan=1, pady=10)

        tk.Label(self, text="Report folder name", font=LARGE_FONT).grid(column=2, row=2, pady=10)
        if(self.image_type + '_folder' in self.database.data):
            ttk.Label(self, text=self.database.data[self.image_type + '_folder']).grid(column=2, row=3, stick='ew')
        else:
            self.entry = ttk.Entry(self, width=5)
            self.entry.grid(column=2, row=3, stick='ew')

        if(self.image_type == 'angle'):
            self.file_count = len(self.database.get_angle_image_paths())
        else:
            self.file_count = len(self.database.get_area_image_paths())

        if(self.file_count > 0):
            string = 'another'
        else:
            string = 'an'
        
        tk.Button(self, text="Add " + string +  " image", width=20, command=self.__get_file).grid(column=2,  row=4, columnspan=1, pady=10)

        if(self.file_count > 1):
            tk.Button(self, text="Generate Report", width=20, command=self.__show_report_page).grid(column=2,  row=5, columnspan=1, pady=10)

        tk.Button(self, text="Back", width=10, command=self.__back).grid(column=2,  row=6, columnspan=1, pady=10)
        tk.Label(self, text= str(self.file_count) + " files added", font=LARGE_FONT).grid(column=2, row=7, columnspan=1, pady=5)
    

    def __get_file(self):
        self.image_file_path = filedialog.askopenfilename(title = "Select tooth image file",
            filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("all files","*.*")), parent=self.parent)
        if(self.image_file_path):
            self.__show_markup_page()

    def __create_project_folder(self):
        if(self.image_type + '_folder' not in self.database.data):
            if(self.entry.get() == ''):
                root_folder = self.image_type.capitalize()
            else:
                root_folder = self.entry.get()
            report_folder_name =  root_folder.replace(' ','_') + '_' + time.strftime('%Y%M%d-%H-%M-%S')
            os.makedirs(report_folder_name)
            self.database.add(self.image_type + '_folder', report_folder_name)
    
    def __show_markup_page(self):
        self.__create_project_folder()
        self.destroy()        
        if(self.image_type == 'angle'):
            self.__show_angle_page()
        else:
            self.__show_area_page()
        self.image_file_path = None        

    def __show_area_page(self):
        frame = GetAreaPage(parent=self.parent, database=self.database, image_path=self.image_file_path)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()
    
    def __show_angle_page(self):
        frame = GetAnglePage(parent=self.parent, database=self.database, image_path=self.image_file_path)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()
    
    def __show_report_page(self):
        self.destroy()
        frame = GenetateReportPage(parent=self.parent, database=self.database, image_type=self.image_type)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()

    def __back(self):
        if(self.file_count > 0):
            if messagebox.askokcancel("Warning", "There are unsaved images. Do you want to clear ?"):
                if(self.image_type == 'angle'):
                    self.database.clear_angle()
                else:
                    self.database.clear_area()
                self.destroy()
        else:
            self.destroy()
        
        