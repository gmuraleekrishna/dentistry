import matplotlib
matplotlib.use("TkAgg")

import tkinter as tk
from tkinter import ttk
import cv2

from get_area_page import GetAreaPage
from get_angle_page import GetAnglePage

LARGE_FONT= ("Verdana", 12)

class Dentistry(tk.Frame):

    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.pack()
        
        self.container = tk.Frame(self, width=200, height=200)
        self.container.pack_propagate(True)
        self.container.pack(side="top", fill="both", expand = True)

        frame = StartPage(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

        
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        ttk.Button(self, text="Calc Angle", command=self.__show_angle_page).pack()

        ttk.Button(self, text="Calc Area", command=self.__show_area_page).pack()

    def __show_area_page(self):
        self.grid_forget()
        frame = GetAreaPage(self.parent, self)
        frame.grid(row=0,column=0,sticky="nsew")
        frame.tkraise()
    
    def __show_angle_page(self):
        self.grid_forget()
        frame = GetAnglePage(self.parent, self)
        frame.grid(row=0,column=0,sticky="nsew")
        frame.tkraise()
        

if __name__ == "__main__":
    app = Dentistry()
    app.master.title("Dentistry")
    app.master.minsize(300, 300)
    app.mainloop()
