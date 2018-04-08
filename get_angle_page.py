# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

from multilines import multilines

LARGE_FONT= ("Verdana", 12)

class GetAnglePage(tk.Frame):

    def __init__(self, parent, database):
        self.parent = parent
        self.database = database
        tk.Frame.__init__(self, self.parent, width=100, height=100)
        label = tk.Label(self, text="Calculate Angle", font=LARGE_FONT)
        label.grid(column=2, row=0, columnspan=1, pady=10)

        self.select_file_btn = tk.Button(self, text="Select tooth image file", width=20, command=self.get_file)
        self.select_file_btn.grid(column=2,  row=1, columnspan=1, pady=10)

        self.back_btn = tk.Button(self, text="Back", width=10, command=self.__back)
        self.back_btn.grid(column=2,  row=2, columnspan=1, pady=10)

        file_count = len(self.database.get_angle_image_paths())
        self.file_nos_label = tk.Label(self, text= str(file_count) + " files added", font=LARGE_FONT)
        self.file_nos_label.grid(column=2, row=5, columnspan=1, pady=5)

    def get_file(self):
        angle_image_file_path = filedialog.askopenfilename(title = "Select tooth image file",
            filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("all files","*.*")), parent=self.parent)
        if(angle_image_file_path):
            self.select_file_btn.destroy()
            self.back_btn.destroy()
            self.file_nos_label.destroy()

            f = Figure(figsize=(6,6), dpi=150)
            a = f.add_subplot(111)
            a.axis('off')
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()

            self.image = cv2.imread(angle_image_file_path)
            a.imshow(self.image)
            self.marked_image = multilines(canvas=canvas, roicolor='r', callback=self.__done_callback)

            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.grid(column=0,  row=3, columnspan=5, sticky='ew', pady=1)

            self.done_btn = tk.Button(self, text="Done", width=10, command=self.__back)
            self.done_btn.grid(column=2,  row=7, columnspan=1, pady=2)
        
    def __done_callback(self):
        file_name = 'angle_'  + str(random.randint(0, 1000)) + '.png'
        angles = []
        lines = self.marked_image.get_lines()

        for line in lines:
            y = np.absolute(line[3] - line[1])
            x = np.absolute(line[2] - line[0])
            angles.append(np.rad2deg(np.arctan2(y, x)))

            self.image = cv2.line(self.image, (int(line[0]), int(line[1])), (int(line[2]), int(line[3])), color=(255, 0, 0), thickness=2, lineType=8)
        angle1 = int(180 - angles[0])
        angle2 = int(180 - angles[1])
        tk.Label(self, text='Angle 1: ' +  str(angle1) + '°', font=LARGE_FONT).grid(column=2, row=4, columnspan=1, pady=2)
        tk.Label(self, text='Angle 2: ' +  str(angle2) + '°', font=LARGE_FONT).grid(column=2, row=5, columnspan=1, pady=2)
        self.database.add_angles(file_name, values=(angle1, angle2))
        cv2.imwrite(file_name, self.image)


    def __back(self):
        self.destroy()

    def index_to_type(self, index):
        return ('preparation', 'after_restoration', 'after_one_day', 'after_4_weeks')[index]