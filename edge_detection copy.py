import cv2
import time
import numpy as np

img = cv2.imread('lowres.jpg')

# cv2.imshow('Original', img) 
# cv2.waitKey(0)


img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.GaussianBlur(img_gray, (13,13), 0)

edges = cv2.Canny(image=img, threshold1=0, threshold2=40) # Canny Edge Detection


cv2.imwrite("out.jpg", edges)