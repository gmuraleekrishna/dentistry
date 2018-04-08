# -*- coding: utf-8 -*-

import matplotlib as mlb
from matplotlib.figure import Figure
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

from roipoly import roipoly
from generate_report_page import GenetateReportPage

LARGE_FONT= ("Verdana", 12)

class GetAreaPage(tk.Frame):

    def __init__(self, parent, database):
        self.parent = parent
        self.database = database
        tk.Frame.__init__(self, self.parent, width=100, height=100)
        label = tk.Label(self, text="Calculate Area", font=LARGE_FONT)
        label.grid(column=2, row=0, columnspan=1, pady=10)

        self.select_file_btn = tk.Button(self, text="Select tooth image file", width=20, command=self.get_file)
        self.select_file_btn.grid(column=2,  row=1, columnspan=1, pady=10)

        self.back_btn = tk.Button(self, text="Back", width=10, command=self.__back)
        self.back_btn.grid(column=2,  row=3, columnspan=1, pady=10)

        file_count = len(self.database.get_area_image_paths())
        self.file_nos_label = tk.Label(self, text= str(file_count) + " files added", font=LARGE_FONT)
        self.file_nos_label.grid(column=2, row=5, columnspan=1, pady=5)

    def get_file(self):
        area_image_file_path = filedialog.askopenfilename(title = "Select tooth image file",
            filetypes = (("jpeg files","*.jpg"),("png files","*.png"), ("all files","*.*")), parent=self.parent)
        if(area_image_file_path):

            self.select_file_btn.destroy()
            self.back_btn.destroy()
            self.file_nos_label.destroy()

            f = Figure(figsize=(6,6), dpi=100)
            a = f.add_subplot(111)
            a.axis('off')
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()

            self.image = cv2.imread(area_image_file_path)
            a.imshow(self.image)
            self.marked_image = roipoly(canvas=canvas, roicolor='r', callback=self.__done_callback)

            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.grid(column=0,  row=3, columnspan=5, sticky='ew', pady=1)

            self.done_btn = tk.Button(self, text="Done", width=10, command=self.__back)
            self.done_btn.grid(column=2,  row=7, columnspan=1, pady=2)
            
    def __done_callback(self):
        file_name = 'area_'  + str(random.randint(0, 1000)) + '.png'
        self.marked_image.finish_drawing()
        roi_pixels = self.marked_image.get_mask(self.image[:,:,0])
        roi_pixels = np.array(roi_pixels, dtype=np.uint8)
        pts = self.marked_image.get_marked_polygon()
        final = cv2.polylines(self.image, [pts], True, color=(255,0, 0), thickness=2, lineType=8)
        cv2.imwrite(file_name, final)
        m = cv2.moments(roi_pixels)

        self.database.add_area(file_name, value=m['m00'])
        area_label = tk.Label(self, text= 'Area: '+ str(m['m00']) + ' px', font=LARGE_FONT, width=25)
        area_label.grid(column=2, row=4, columnspan=1, pady=5)
    
    def __back(self):
        self.destroy()
