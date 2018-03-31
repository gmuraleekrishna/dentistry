import matplotlib
matplotlib.use('TkAgg')

import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.figure import Figure

from roipoly import roipoly

LARGE_FONT= ("Verdana", 12)

class GetAreaPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Area", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        f = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvasTkAgg(f, master=parent)
       
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.get_area(figure=f, canvas=canvas)
      
    #     canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    #     # toolbar = NavigationToolbar2TkAgg(canvas, self)
    #     # toolbar.update()
    #     # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def get_area(self, figure, canvas):
        img = cv2.imread("tooth_top.png")
        a = figure.add_subplot(111)
        a.imshow(img)

        im = roipoly(canvas=canvas, roicolor='r')

  
        # # tkagg.blit(img, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        # roi_pixels = im.getMask(im[:,:,0])
        # roi_pixels = np.array(roi_pixels, dtype=np.uint8)
        # m = cv2.moments(roi_pixels)

        # print(m['m00'])
    