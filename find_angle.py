
from roipoly import roipoly
from multilines import multilines
import matplotlib.pyplot as plt
import cv2
import numpy as np

img = cv2.imread("tooth_side.png")
plt.imshow(img)
lines = multilines(roicolor='r').get_lines()

for line in lines:
    y = np.absolute(line[3] - line[1])
    x = np.absolute(line[2] - line[0])
    angle = np.rad2deg(np.arctan2(y, x))
    print(angle)
