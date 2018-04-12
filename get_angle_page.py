# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import os

from multilines import multilines

LARGE_FONT= ("Verdana", 12)


class GetAnglePage(tk.Frame):

    def __init__(self, parent, database, image_path):
        self.parent = parent
        self.database = database
        self.image_path = image_path
        tk.Frame.__init__(self, self.parent, width=100, height=100)
        tk.Label(self, text="Calculate Angle", font=LARGE_FONT).grid(column=2, row=0, columnspan=1, pady=10)
        tk.Label(self, text="Click on the image to draw").grid(column=2, row=1, columnspan=1, pady=10)

        f = Figure(figsize=(6,6), dpi=100)
        a = f.add_subplot(111)
        a.axis('off')
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()

        self.image = cv2.imread(self.image_path)
        a.imshow(self.image)
        self.marked_image = multilines(canvas=canvas, roicolor='r', callback=self.__done_callback)

        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.grid(column=0,  row=3, columnspan=5, sticky='ew', pady=1)

        self.done_btn = tk.Button(self, text="Done", width=10, command=self.__back)
        self.done_btn.grid(column=2,  row=7, columnspan=1, pady=2)
        
    def __done_callback(self):
        file_path =  os.path.join(self.database.data['angle_folder'], str(random.randint(0, 1000)) + '.png')
        angles = []
        lines = self.marked_image.get_lines()
        lowest_point = []
        for line in lines:
            y = np.absolute(line[3] - line[1])
            x = np.absolute(line[2] - line[0])
            angles.append(np.rad2deg(np.arctan2(y, x)))

            self.image = cv2.line(self.image, ( line[0], line[1] ), ( line[2], line[3] ), color=(255, 0, 0), thickness=2, lineType=8)
            if(line[3] > line[1]):
                lowest_point.append((line[2] , line[3]))
            else:
                lowest_point.append((line[0] , line[1]))

        angle1 = int(180 - angles[0])
        angle2 = int(180 - angles[1])
        font = cv2.FONT_HERSHEY_PLAIN
        if(lowest_point[0][1] > lowest_point[1][1]):
            cv2.putText(self.image, str(angle1) ,(lowest_point[1][0] + 6,  lowest_point[1][1] - 18), font, 0.7, (0 ,0, 255), 1, cv2.LINE_AA)
            cv2.putText(self.image, str(angle2) ,(lowest_point[0][0] - 18,  lowest_point[1][1] - 18), font, 0.7, (0 ,0, 255), 1, cv2.LINE_AA)
            self.image = cv2.line(self.image, (15, lowest_point[1][1] - 10), (self.image.shape[1] - 15, lowest_point[1][1] - 10), color=(0, 0, 255), thickness=2, lineType=8)
        else:
            cv2.putText(self.image, str(angle1) ,(lowest_point[0][0] + 6,  lowest_point[0][1] - 18), font, 0.7, (0 ,0, 255), 1, cv2.LINE_AA)
            cv2.putText(self.image, str(angle2) ,(lowest_point[1][0] - 18,  lowest_point[0][1] - 18), font, 0.7, (0 ,0, 255), 1, cv2.LINE_AA)
            self.image = cv2.line(self.image, (15, lowest_point[0][1] - 10), (self.image.shape[1] - 15, lowest_point[0][1] - 10), color=(0, 0, 255), thickness=2, lineType=8)
        
        tk.Label(self, text='Angle 1: ' +  str(angle1) + '°', font=LARGE_FONT).grid(column=2, row=4, columnspan=1, pady=2)
        tk.Label(self, text='Angle 2: ' +  str(angle2) + '°', font=LARGE_FONT).grid(column=2, row=5, columnspan=1, pady=2)
        self.database.add_angles(file_path, values=(angle1, angle2))
        cv2.imwrite(file_path, self.image)

    def __back(self):
        self.destroy()
        from get_image_file_page import GetImageFilePage
        frame = GetImageFilePage(parent=self.parent, database=self.database, image_type='angle')
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()