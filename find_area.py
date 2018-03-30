from roipoly import roipoly
import matplotlib.pyplot as plt
import cv2
import numpy as np

img = cv2.imread("tooth_top.png")
plt.imshow(img)
im = roipoly(roicolor='r')

roi_pixels = im.getMask(img[:,:,0])
plt.imshow(roi_pixels)
roi_pixels = np.array(roi_pixels, dtype=np.uint8)
m = cv2.moments(roi_pixels)

print(m['m00'])