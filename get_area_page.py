from matplotlib.figure import Figure
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from roipoly import roipoly

LARGE_FONT= ("Verdana", 12)

class GetAreaPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Calculate Area", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.select_file_btn = tk.Button(self, text="Select file", command=self.get_file)
        self.select_file_btn.pack()
        self.back_btn = tk.Button(self, text="Cancel", command=self.back)
        self.back_btn.pack()
        self.pack()

    def get_file(self):
        area_image_file_path = filedialog.askopenfilename(title = "Select tooth image file", filetypes = (("jpeg files","*.jpg"),("png files","*.png"), ("all files","*.*")))
        if(area_image_file_path):
            self.select_file_btn.destroy()
            f = Figure(figsize=(5,5), dpi=100)
            a = f.add_subplot(111)
            a.axis('off')
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            self.image = cv2.imread(area_image_file_path)
            a.imshow(self.image)
            self.marked_image = roipoly(canvas=canvas, roicolor='r', callback=self.__done_callback)
            tk.Button(self, text="Done", command=self.__done_callback).pack()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def __done_callback(self):
        self.marked_image.finish_drawing()
        roi_pixels = self.marked_image.get_mask(self.image[:,:,0])
        roi_pixels = np.array(roi_pixels, dtype=np.uint8)
        m = cv2.moments(roi_pixels)
        area_label = tk.Label(self, text=m['m00'], font=LARGE_FONT)
        area_label.pack(pady=10,padx=10)
    def back(self):
        self.destroy()
