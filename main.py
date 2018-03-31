import tkinter as tk
from tkinter import ttk
import sys

from start_page import StartPage
from get_angle_page import GetAnglePage
from get_area_page import GetAreaPage

LARGE_FONT= ("Verdana", 12)

class DentistryApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Dentistry")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        frame = GetAreaPage(container, self)
        frame.tkraise()



def main():
    app = DentistryApp()
    def kill_pgm():
        app.destroy()
        sys.exit(0)
    
    app.protocol("WM_DELETE_WINDOW", kill_pgm)
    app.bind('<Escape>', kill_pgm)
    app.mainloop()



if __name__ == "__main__":
    main()

