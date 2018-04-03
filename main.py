import matplotlib
matplotlib.use("TkAgg")

import tkinter as tk
from tkinter import ttk
import cv2

from get_area_page import GetAreaPage
from get_angle_page import GetAnglePage

LARGE_FONT= ("Verdana", 12)

class Dentistry(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, GetAnglePage, GetAreaPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        angle_page_btn = ttk.Button(self, text="Calc Angle",
                            command=lambda: controller.show_frame(GetAnglePage))
        angle_page_btn.pack()

        area_page_btn = ttk.Button(self, text="Calc Area",
                            command=lambda: controller.show_frame(GetAreaPage))
        area_page_btn.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(GetAnglePage))
        button2.pack()
    
        
if __name__ == "__main__":
    app = Dentistry()
    app.mainloop()
