import matplotlib
matplotlib.use('TkAgg')
import cv2
from matplotlib.figure import Figure
from roipoly import roipoly
import tkinter as tk
from tkinter import ttk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


LARGE_FONT= ("Verdana", 12)

class GetAreaPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        
        label.pack(pady=10,padx=10)

        # button1 = ttk.Button(self, text="Done", command=lambda: controller.show_frame(StartPage))
        # button1.pack()

        

        f = Figure(figsize=(5,5), dpi=100)

        self.image = cv2.imread("tooth_top.png")
        a = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        a.imshow(self.image)
        self.marked_image = roipoly(canvas=canvas, roicolor='r', callback=self.__done_callback)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        done_button = ttk.Button(self, text="Done", command=self.__done_callback)
        done_button.pack()
        
    
    def __done_callback(self):
        self.marked_image.finish_drawing()
        roi_pixels = self.marked_image.get_mask(self.image[:,:,0])
        roi_pixels = np.array(roi_pixels, dtype=np.uint8)
        m = cv2.moments(roi_pixels)

        print(m['m00'])
