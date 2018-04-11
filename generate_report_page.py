# -*- coding: utf-8 -*-

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import utils
    
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import os

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
        file_path = os.path.join(self.database.data[self.image_type + '_folder'],  self.image_type + "_report_" + time.strftime('%Y-%m-%d-%H%M%S') + ".pdf")
        doc = SimpleDocTemplate(file_path, pagesize=A4,
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
                im = self.get_image(area_image, width=2.5*inch)
                Story.append(im)
                area_text = '<font size=11>Area: %s pixels</font>' % area
                
                Story.append(Paragraph(area_text, styles["Normal"]))
                Story.append(Spacer(1, 24))
            areas = list(self.database.area_values.items())
            if(len(areas) > 1):
                first_area = areas[0][1]
                last_area = areas[-1][1]
                if(first_area > last_area):
                    state = 'reduced'
                elif (first_area < last_area):
                    state = 'increased'
                else:
                    state =  'unchanged'
                percentage = 100.0 * math.fabs(last_area - first_area) / first_area
                analysis = "The area has %s by %0.1f %%" % (state, percentage)
                Story.append(Paragraph("Analysis: " + analysis, styles["Normal"]))
                Story.append(Spacer(1, 12))
            self.database.clear_area()
        elif(self.image_type == 'angle'):
            for angle_image in self.database.get_angle_image_paths():
                im = self.get_image(angle_image, width=2.5*inch)
                Story.append(im)
                angle1 = self.database.angle_values[angle_image][0]
                angle2 =self.database.angle_values[angle_image][1]
                angle1 = "<font size=12>Angle1:  %s°</font>" % angle1
                angle2 = "<font size=12>Angle2:  %s°</font>" % angle2
                
                Story.append(Paragraph(angle1, styles["Normal"]))
                Story.append(Spacer(1, 12))
                Story.append(Paragraph(angle2, styles["Normal"]))
                Story.append(Spacer(1, 24))
            angles = list(self.database.angle_values.items())
            if(len(angles) > 1):
                first_angles = angles[0][1]
                last_angles = angles[-1][1]
                state1, percentage1 = self.get_change(first_angles[0], last_angles[0])
                state2, percentage2 = self.get_change(first_angles[1], last_angles[1])
                analysis1 = "Angle1 has %s by %0.1f %%" % (state1, percentage1)
                analysis2 = "angle2 has %s by %0.1f %%" % (state2, percentage2)
                Story.append(Paragraph("Analysis: " + analysis1 + ' and ' +  analysis2, styles["Normal"]))
                Story.append(Spacer(1, 12))
            self.database.clear_angle()
        Story.append(Paragraph("Comment: " + self.entry.get(), styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        doc.build(Story)
        if messagebox.showinfo("Saved", "Report generated: " + file_path):
            self.__back()


    def get_image(self, path, width=1*inch):
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect))
        
    def get_change(self, first_angle, last_angle):
        if(first_angle > last_angle):
            state = 'reduced'
        elif (first_angle < last_angle):
            state = 'increased'
        else:
            state =  'unchanged'
        percentage = 100.0 * math.fabs(first_angle - last_angle) / first_angle
        return state, percentage
    def __back(self):
        self.destroy()



 
 
