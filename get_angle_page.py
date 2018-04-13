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

        tk.Label(self, text="Click on the image to draw").pack(side = tk.TOP, pady=10)

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
        self.marked_image = multilines(canvas=self.canvas, roicolor='r', callback=self.__done_callback)

        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(width=500, height=500, bd=0, highlightthickness=0, relief='flat',  borderwidth=0)
        self.canvas_widget.pack(side = tk.BOTTOM, pady=0)

        self.angle_label = tk.Label(self, text='', font=LARGE_FONT)
        self.angle_label.pack(side = tk.BOTTOM, pady=10)


        
        
    def __done_callback(self):
        self.done_btn.config(state='active')
        file_path =  os.path.join(self.database.data['angle_folder'], str(random.randint(0, 1000)) + '.png')
        angles = []
        lines = self.marked_image.get_lines()
        lowest_point = []
        for line in lines:
            y = line[3] - line[1]
            x = line[2] - line[0]
            angles.append(np.rad2deg(np.arctan2(y, x)))

            self.image = cv2.line(self.image, ( line[0], line[1] ), (line[2], line[3] ), color=(255, 0, 0), thickness=2, lineType=8)
            if(line[3] > line[1]):
                lowest_point.append((line[2] , line[3]))
            else:
                lowest_point.append((line[0] , line[1]))

        angle1 = int(180- angles[0])
        angle2 = int(angles[1])
        font = cv2.FONT_HERSHEY_PLAIN
        if(lowest_point[0][1] > lowest_point[1][1]):
            self.image = cv2.line(self.image, (15, lowest_point[1][1] - 10), (self.image.shape[1] - 15, lowest_point[1][1] - 10), color=(255, 0, 255), thickness=1, lineType=8)
            cv2.putText(self.image, str(angle2) ,(lowest_point[1][0] -18,  lowest_point[1][1] - 18), font, 0.7, (0 ,0, 255), 1, cv2.LINE_AA)
            cv2.putText(self.image, str(angle1) ,(lowest_point[0][0] - 6,  lowest_point[1][1] - 18), font, 0.7, (0 ,255, 0), 1, cv2.LINE_AA)
        else:
            self.image = cv2.line(self.image, (15, lowest_point[0][1] - 10), (self.image.shape[1] - 15, lowest_point[0][1] - 10), color=(255, 0, 255), thickness=1, lineType=8)
            cv2.putText(self.image, str(angle1) ,(lowest_point[0][0] + 6,  lowest_point[0][1] - 18), font, 0.7, (0 ,0, 255), 1, cv2.LINE_AA)
            cv2.putText(self.image, str(angle2) ,(lowest_point[1][0] - 18,  lowest_point[0][1] - 18), font, 0.7, (0 , 255, 0), 1, cv2.LINE_AA)
        
        self.angle_label.config(text='Angle 1: ' +  str(angle1) + '°, Angle 2: ' +  str(angle2) + '°')
        self.a.imshow(self.image)
        self.canvas.draw()
        self.database.add_angles(file_path, values=(angle1, angle2))
        cv2.imwrite(file_path, self.image)

    def __back(self):
        self.destroy()
        from get_image_file_page import GetImageFilePage
        frame = GetImageFilePage(parent=self.parent, database=self.database, image_type='angle')
        frame.grid(column=0, row=0, sticky='nsew')
        frame.lift()