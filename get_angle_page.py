from matplotlib.figure import Figure
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

from multilines import multilines

LARGE_FONT= ("Verdana", 12)

class GetAnglePage(tk.Frame):

    def __init__(self, parent, controller, database):
        self.parent = parent
        self.database = database
        tk.Frame.__init__(self, self.parent)
        label = tk.Label(self, text="Calculate Angle", font=LARGE_FONT)
        label.grid(column=6, row=0, columnspan=1, pady=5)

        self.box = ttk.Combobox(self.parent, state='readonly')
        self.box.grid(column=0, row=1, columnspan=2, pady=5, padx=5, in_=self.parent)
        self.box['values'] = ('Preparation', 'After Restoration', 'After 1day', 'After 4weeks')
        self.box.current(0)

        self.select_file_btn = tk.Button(self, text="Select file", width=10, command=self.get_file)
        self.select_file_btn.grid(column=6,  row=4, columnspan=1, pady=5)

        self.back_btn = tk.Button(self, text="Cancel", width=10, command=self.__back)
        self.back_btn.grid(column=6,  row=5, columnspan=1, pady=5)
        self.pack()

    def get_file(self):
        angle_image_file_path = filedialog.askopenfilename(title = "Select tooth image file",
            filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("all files","*.*")), parent=self.parent)
        if(angle_image_file_path):
            self.select_file_btn.destroy()
            self.back_btn.destroy()
            self.type_of_tooth_image_index =  self.box.current()
            self.box.destroy()

            f = Figure(figsize=(5,5), dpi=100)
            a = f.add_subplot(111)
            a.axis('off')
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()

            self.image = cv2.imread(angle_image_file_path)
            a.imshow(self.image)
            self.marked_image = multilines(canvas=canvas, roicolor='r', callback=self.__done_callback)

            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.grid(column=3,  row=3, columnspan=5, sticky='ew')

            self.done_btn = tk.Button(self, text="Done", width=10, command=self.__back)
            self.done_btn.grid(column=5,  row=7, columnspan=2, pady=5)
        
    def __done_callback(self):
        type_of_tooth_image = self.index_to_type(self.type_of_tooth_image_index)
        file_name = 'angle_'  + type_of_tooth_image + '.png'
        angles = []
        lines = self.marked_image.get_lines()

        for line in lines:
            y = np.absolute(line[3] - line[1])
            x = np.absolute(line[2] - line[0])
            angles.append(np.rad2deg(np.arctan2(y, x)))

            self.image = cv2.line(self.image, (math.floor(line[0]), math.floor(line[1])), (math.floor(line[2]), math.floor(line[3])), color=(255, 0, 0), thickness=2, lineType=8)
        tk.Label(self, text='Angle 1: ' + str(math.floor(angles[0])), font=LARGE_FONT).grid(column=5, row=5, columnspan=1, pady=5)
        tk.Label(self, text='Angle 2: ' +  str(math.floor(angles[1])), font=LARGE_FONT).grid(column=5, row=6, columnspan=1, pady=5)
        cv2.imwrite(file_name, self.image)
        self.database.add_angles(type_of_tooth_image, file_name, values=angles)


    def __back(self):
        self.destroy()

    def index_to_type(self, index):
        return ('preparation', 'after_restoration', 'after_one_day', 'after_4_weeks')[index]