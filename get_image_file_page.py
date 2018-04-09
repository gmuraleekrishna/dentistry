from tkinter import filedialog
import tkinter as tk
from tkinter import ttk

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


        if(self.image_type == 'angle'):
            file_count = len(self.database.get_angle_image_paths())
        else:
            file_count = len(self.database.get_area_image_paths())
        
        if(file_count > 0):
            string = 'another'
            tk.Button(self, text="Generate Report", width=20, command=self.__show_report_page).grid(column=2,  row=2, columnspan=1, pady=10)
        else:
            string = 'an'

        tk.Label(self, text="Calculate " + image_type.capitalize(), font=LARGE_FONT).grid(column=2, row=0, columnspan=1, pady=10)

        tk.Button(self, text="Add " + string +  " image", width=20, command=self.__get_file).grid(column=2,  row=1, columnspan=1, pady=10)


        tk.Button(self, text="Back", width=10, command=self.__back).grid(column=2,  row=3, columnspan=1, pady=10)

  
        tk.Label(self, text= str(file_count) + " files added", font=LARGE_FONT).grid(column=2, row=5, columnspan=1, pady=5)
    

    def __get_file(self):
        self.image_file_path = filedialog.askopenfilename(title = "Select tooth image file",
            filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("all files","*.*")), parent=self.parent)
        if(self.image_file_path):
            self.__show_markup_page()


    def __show_markup_page(self):
        self.lower()
        if(self.image_type == 'angle'):
            self.__show_angle_page()
        else:
            self.__show_area_page()

    def __show_area_page(self):
        frame = GetAreaPage(parent=self.parent, database=self.database, image_path=self.image_file_path)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()
    
    def __show_angle_page(self):
        # self.lower()
        frame = GetAnglePage(parent=self.parent, database=self.database, image_path=self.image_file_path)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()
    
    def __show_report_page(self):
        self.destroy()
        frame = GenetateReportPage(parent=self.parent, database=self.database, image_type=self.image_type)
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()

    def __back(self):
        self.destroy()
        