
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import cv2
import numpy as np

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from multilines import multilines


LARGE_FONT= ("Verdana", 12)

class GetAnglePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Angle", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        f = Figure(figsize=(5,5), dpi=100)

        self.image = cv2.imread("tooth_top.png")
        a = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        a.imshow(self.image)
        self.marked_image = multilines(canvas=canvas, roicolor='r', callback=self.__done_callback)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        done_button = ttk.Button(self, text="Done", command=self.__done_callback)
        done_button.pack()

    def __done_callback(self):
        angle = []
        for line in self.marked_image.get_lines():
            y = np.absolute(line[3] - line[1])
            x = np.absolute(line[2] - line[0])
            angle.append(np.rad2deg(np.arctan2(y, x)))
            
        tk.Label(self, text=angle[0], font=LARGE_FONT).pack(pady=10,padx=10)
        tk.Label(self, text=angle[1], font=LARGE_FONT).pack(pady=10,padx=10)