# -*- coding: utf-8 -*-

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
import time
import io
import tkinter as tk
from tkinter import ttk, StringVar

LARGE_FONT= ("Verdana", 12)

class GenetateReportPage(tk.Frame):

    def __init__(self, parent, database, image_type):
        self.parent = parent
        self.database = database
        self.image_type = image_type
        tk.Frame.__init__(self, self.parent, width=100, height=100)
        tk.Label(self, text="Generate PDF Report", font=LARGE_FONT).grid(column=2, row=0, pady=10)

        tk.Label(self, text="Add a comment", font=LARGE_FONT).grid(column=2, row=4, pady=10)
        self.entry = ttk.Entry(self, width=25)
        self.entry.grid(column=2, row=5, stick='ew')

        self.gen_report_btn = tk.Button(self, text="Generate PDF", width=20, command=self.gen_report).grid(column=2, row=7, pady=10)

        self.back_btn = tk.Button(self, text="Back", width=10, command=self.__back).grid(column=2, row=8, pady=10)

        self.pack()

    def gen_report(self):
        file_name = self.image_type + "_" + time.strftime('%Y-%m-%d%H%M%S') + ".pdf"
        doc = SimpleDocTemplate(file_name, pagesize=A4,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
        Story=[]
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Left', alignment=TA_JUSTIFY))
        Story.append(Paragraph(self.image_type.capitalize() + " Report", styles["Heading1"]))
        Story.append(Spacer(1, 12))

        if(self.image_type == 'area'):
            for area_image in self.database.get_area_image_paths():
                area = self.database.area_values[area_image]
                im = Image(area_image, 2*inch, 2*inch)
                Story.append(im)
                area_text = '<font size=12>Area %s pixels</font>' % area
                
                Story.append(Paragraph(area_text, styles["Normal"]))
                Story.append(Spacer(1, 24))

        elif(self.image_type == 'angle'):
            for angle_image in self.database.get_angle_image_paths():
                im = Image(angle_image, 2*inch, 2*inch)
                Story.append(im)
                angle1 = self.database.angle_values[angle_image][0]
                angle2 =self.database.angle_values[angle_image][1]
                angle1 = "<font size=12>Angle1:  %s°</font>" % angle1
                angle2 = "<font size=12>Angle2:  %s°</font>" % angle2
                
                Story.append(Paragraph(angle1, styles["Normal"]))
                Story.append(Spacer(1, 12))
                Story.append(Paragraph(angle2, styles["Normal"]))
                Story.append(Spacer(1, 24))
        

        Story.append(Paragraph("Comment: " + self.entry.get(), styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        doc.build(Story)
        
        tk.Label(self, text="Report generated: " + file_name, font=LARGE_FONT).grid(column=2, row=10, pady=10)
    
    def __back(self):
        self.destroy()



 
 
