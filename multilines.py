import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.path as mplPath


class multilines:

    def __init__(self, canvas, roicolor='b', max_lines=2):
        self.previous_point = []
        self.start_point = []
        self.line = None
        self.roicolor = roicolor
        self.canvas = canvas
        self.lines = []
        self.max_lines = max_lines
        self.no_of_lines = 0

        self.__ID1 = self.canvas.mpl_connect(
            'motion_notify_event', self.__motion_notify_callback
            )
        self.__ID2 = self.canvas.mpl_connect(
            'button_press_event', self.__button_press_callback
            )
        self.__ID3 = self.canvas.mpl_connect(
            'key_press_event', self.__button_press_callback
            )

    def get_lines(self):
        return self.lines

    def __motion_notify_callback(self, event):
        if event.inaxes:
            ax = event.inaxes
            x, y = event.xdata, event.ydata
            if (event.button == None or event.button == 1) and self.line != None: # Move line around
                self.line.set_data([self.previous_point[0], x],
                                   [self.previous_point[1], y])
                self.canvas.draw()

    def __button_press_callback(self, event):
        if event.inaxes:
            if event.name == 'button_press_event' and event.button == 1:
                x, y = event.xdata, event.ydata
                ax = event.inaxes
                if event.dblclick == False:
                    if self.line == None:
                        self.line = plt.Line2D([x, x],
                                            [y, y],
                                            color=self.roicolor)
                        self.start_point = [x,y]
                        self.previous_point =  self.start_point                                                
                        ax.add_line(self.line)

                    else:
                        self.line = plt.Line2D([self.previous_point[0], x],
                                            [self.previous_point[1], y],
                                            color=self.roicolor)
                        event.inaxes.add_line(self.line)
                        self.line = None
                        line = (self.previous_point[0], self.previous_point[1], x, y)
                        self.lines.append(line)
                        self.no_of_lines = self.no_of_lines + 1
                        if self.no_of_lines >= self.max_lines:
                            self.__close()
                            return
                    self.canvas.draw()

            elif event.name == 'key_press_event':
                self.__close()
                return
    
    def __close(self):
        self.canvas.mpl_disconnect(self.__ID1)
        self.canvas.mpl_disconnect(self.__ID2)
        self.canvas.mpl_disconnect(self.__ID3)
        return