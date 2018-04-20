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

        self.gen_report_btn = tk.Button(self, text="Generate PDF", width=20, command=self.gen_report)
        self.gen_report_btn.grid(column=2, row=7, pady=10)

        self.back_btn = tk.Button(self, text="Back", width=10, command=self.__back).grid(column=2, row=8, pady=10)

        self.pack()

    def gen_report(self):
        self.gen_report_btn.config(text="Generating...")
        file_path = os.path.join(self.database.data[self.image_type + '_folder'],  self.image_type + "_report_" + time.strftime('%Y%m%d-%H%M%S') + ".pdf")
        doc = SimpleDocTemplate(file_path, pagesize=A4,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
        Story=[]
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Left', alignment=TA_JUSTIFY))
        Story.append(Paragraph("Dent-Reckoner %s Report" % self.image_type.capitalize() , styles["Heading1"]))
        Story.append(Spacer(1, 12))

        if(self.image_type == 'area'):
            areas = self.database.area_values.items()
            first_area = 0
            for index, (image_path, area) in enumerate(areas):
                im = self.get_image(image_path, width=2.5*inch)
                Story.append(im)
                
                Story.append(Paragraph('Area: %s pixels' % area, styles["Normal"]))
                if(index > 0):
                    state, percentage = self.get_change(first_area, area)
                    evaluation = "The area has %s by %0.1f%% compared to first image" % (state, percentage)
                    Story.append(Paragraph(evaluation, styles["Normal"]))
                else:
                    first_area = area
                Story.append(Spacer(1, 24))

            areas = list(self.database.area_values.items())
            if(len(areas) > 0):
                first_area = areas[0][1]
                last_area = areas[-1][1]
                state, percentage = self.get_change(first_area, last_area)
                analysis = "The area has %s by %0.1f%%" % (state, percentage)
                Story.append(Paragraph("Summary: " + analysis, styles["Normal"]))
                Story.append(Spacer(1, 12))
            self.database.clear_area()
        elif(self.image_type == 'angle'):
            angles = list(self.database.angle_values.items())
            first_angles = (0, 0)
            for index, (image_path, angle_pair) in enumerate(angles):
                im = self.get_image(image_path, width=2.5*inch)
                Story.append(im)
                angle1 = angle_pair[0]
                angle2 = angle_pair[1]
                
                Story.append(Paragraph("Angle1:  %s°, Angle2: %s°" % (angle1, angle2), styles["Normal"]))
                if(index > 0):
                    state1, percentage1 = self.get_change(first_angles[0], angle1)
                    state2, percentage2 = self.get_change(first_angles[1], angle2)
                    evaluation1 = "Angle1 has %s by %0.1f%%" % (state1, percentage1)
                    evaluation2 = "Angle2 has %s by %0.1f%%" % (state2, percentage2)
                    Story.append(Paragraph("Analysis: %s and %s compared to first image" % (evaluation1, evaluation2), styles["Normal"]))
                else:
                    first_angles = (angle1, angle2)

                Story.append(Spacer(1, 24))
            if(len(angles) > 1):
                first_angles = angles[0][1]
                last_angles = angles[-1][1]
                state1, percentage1 = self.get_change(first_angles[0], last_angles[0])
                state2, percentage2 = self.get_change(first_angles[1], last_angles[1])
                analysis1 = "Angle1 has %s by %0.1f %%" % (state1, percentage1)
                analysis2 = "angle2 has %s by %0.1f %%" % (state2, percentage2)
                Story.append(Paragraph("Summary: %s and %s" % (analysis1, analysis2), styles["Normal"]))
                Story.append(Spacer(1, 12))
            self.database.clear_angle()
        Story.append(Paragraph("Comment: " + self.entry.get(), styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        doc.build(Story)
        self.gen_report_btn.config(text="Generate PDF")
        if messagebox.showinfo("Saved", "Report generated at " + file_path):
            self.__back()


    def get_image(self, path, width=1*inch):
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect))
        
    def get_change(self, first_value, second_value):
        if(first_value > second_value):
            state = 'reduced'
        elif (first_value < second_value):
            state = 'increased'
        else:
            state =  'remain unchanged'
        percentage = 100.0 * math.fabs(first_value - second_value) / first_value
        return state, percentage
    def __back(self):
        self.destroy()



 
 
