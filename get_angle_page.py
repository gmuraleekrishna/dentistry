from matplotlib.figure import Figure
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from multilines import multilines

LARGE_FONT= ("Verdana", 12)

class GetAnglePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Calculate Angle", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.select_file_btn = tk.Button(self, text="Select file", command=self.get_file)
        self.select_file_btn.pack()

        self.back_btn = tk.Button(self, text="Cancel", command=self.back)
        self.back_btn.pack()

        self.pack()

    def get_file(self):
        angle_image_file_path = filedialog.askopenfilename(title = "Select tooth image file", filetypes = (("jpeg files","*.jpg"),("png files","*.png"), ("all files","*.*")))
        if(angle_image_file_path):
            self.select_file_btn.destroy()
            f = Figure(figsize=(5,5), dpi=100)
            a = f.add_subplot(111)
            a.axis('off')
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            self.image = cv2.imread(angle_image_file_path)
            a.imshow(self.image)
            self.marked_image = multilines(canvas=canvas, roicolor='r', callback=self.__done_callback)
            tk.Button(self, text="Done", command=self.__done_callback).pack()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
    def __done_callback(self):
        angle = []
        for line in self.marked_image.get_lines():
            y = np.absolute(line[3] - line[1])
            x = np.absolute(line[2] - line[0])
            angle.append(np.rad2deg(np.arctan2(y, x)))
        tk.Label(self, text=angle[0], font=LARGE_FONT).pack(pady=10,padx=10).pack()
        tk.Label(self, text=angle[1], font=LARGE_FONT).pack(pady=10,padx=10).pack()
    def back(self):
        self.destroy()