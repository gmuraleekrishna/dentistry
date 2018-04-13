# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import os

from roipoly import roipoly


LARGE_FONT= ("Verdana", 12)

class GetAreaPage(tk.Frame):

    def __init__(self, parent, database, image_path):
        self.parent = parent
        self.database = database
        self.image_path = image_path
        tk.Frame.__init__(self, self.parent, width=100, height=100)
        tk.Label(self, text="Click on the image to draw. Double click to finish drawing").pack(side = tk.TOP, pady=10)

        self.done_btn = tk.Button(self, text="Done", width=10, command=self.__back)
        self.done_btn.config(state='disabled')
        self.done_btn.pack(side = tk.TOP, pady=0)
        

        f = Figure(figsize=(6,6), dpi=100)
        self.a = f.add_subplot(111)
        self.a.axis('off')
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()

        self.image = cv2.imread(self.image_path)
        self.a.imshow(self.image)
        self.marked_image = roipoly(canvas=self.canvas, roicolor='r', callback=self.__done_callback)

        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(width=500, height=500, bd=0, highlightthickness=0, relief='flat',  borderwidth=0)
        self.canvas_widget.pack(side = tk.BOTTOM, pady=0)

        self.area_label = tk.Label(self, text='', font=LARGE_FONT)
        self.area_label.pack(side = tk.BOTTOM, pady=10)

            
    def __done_callback(self):
        self.done_btn.config(state='active')
        file_path =  os.path.join(self.database.data['area_folder'], str(random.randint(0, 1000)) + '.png')
        self.marked_image.finish_drawing()
        roi_pixels = self.marked_image.get_mask(self.image[:,:,0])
        roi_pixels = np.array(roi_pixels, dtype=np.uint8)
        pts = self.marked_image.get_marked_polygon()
        final = cv2.polylines(self.image, [pts], True, color=(255,0, 0), thickness=2, lineType=8)
        cv2.imwrite(file_path, final)
        m = cv2.moments(roi_pixels)
        self.database.add_area(file_path, value=m['m00'])
        self.area_label.config( text= 'Area: '+ str(m['m00']) + ' px')
        self.a.imshow(self.image)
        self.canvas.draw()

    def __back(self):
        self.destroy()
        from get_image_file_page import GetImageFilePage
        frame = GetImageFilePage(parent=self.parent, database=self.database, image_type='area')
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()
