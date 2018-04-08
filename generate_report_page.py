# -*- coding: utf-8 -*-

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
 
import io
import tkinter as tk
from tkinter import ttk, StringVar

LARGE_FONT= ("Verdana", 12)

class GenetateReportPage(tk.Frame):

    def __init__(self, parent, database):
        self.parent = parent
        self.database = database
        tk.Frame.__init__(self, self.parent, width=100, height=100)
        label = tk.Label(self, text="Generate PDF Report", font=LARGE_FONT)
        label.grid(column=2, row=0, pady=10)

        self.report_type = StringVar()
        self.report_type.set('area')
        tk.Label(self, text="Report type", font=LARGE_FONT).grid(column=2, row=10, columnspan=4)
        ttk.Radiobutton(parent, text='Area', variable=self.report_type, value='area').grid(column=0, row=1, stick='ew', columnspan=3)
        ttk.Radiobutton(parent, text='Angle', variable=self.report_type, value='angle').grid(column=0, row=2, stick='ew', columnspan=3)
        
        self.entry = ttk.Entry(self, width=15).grid(column=2, row=7, stick='ew')

        self.gen_report_btn = tk.Button(self, text="Generate Report", width=20, command=self.gen_report).grid(column=2, row=10, pady=10)

        self.back_btn = tk.Button(self, text="Back", width=10, command=self.__back).grid(column=2, row=11, pady=10)

        self.pack()

    def gen_report(self):
        report_type = self.report_type.get()
        doc = SimpleDocTemplate( report_type + ".pdf", pagesize=A4,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
        Story=[]
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Left', alignment=TA_JUSTIFY))
        Story.append(Paragraph(report_type.capitalize() + " Report", styles["Heading1"]))
        Story.append(Spacer(1, 12))

        if(report_type == 'area'):
            for area_image in self.database.get_area_image_paths():
                area = self.database.area_values[area_image]
                im = Image(area_image, 2*inch, 2*inch)
                Story.append(im)
                area_text = '<font size=12>Area %s pixels</font>' % self.database.area_values[area_image]
                
                Story.append(Paragraph(area_text, styles["Normal"]))
                Story.append(Spacer(1, 24))
        elif(report_type == 'angle'):
            for angle_image in self.database.get_angle_image_paths():
                im = Image(angle_image, 2*inch, 2*inch)
                Story.append(im)
                
                angle1 = '<font size=12>Angle1:  %s \xb0</font>' % self.database.angle_values[angle_image][0]
                angle2 = '<font size=12>Angle2:  %s \xb0</font>' % self.database.angle_values[angle_image][1]
                
                Story.append(Paragraph(angle1, styles["Normal"]))
                Story.append(Spacer(1, 12))
                Story.append(Paragraph(angle2, styles["Normal"]))
                Story.append(Spacer(1, 24))

        doc.build(Story)
    
    def __back(self):
        self.destroy()



 
 
