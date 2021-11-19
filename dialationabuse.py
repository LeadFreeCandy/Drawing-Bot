import cv2 as cv2
import numpy as np
import random as rd
import time
import math
import sys
import pickle
import facemesh
import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename

blur_radius = 15 # must be an odd number
face_blur_radius = 5
lower_thresh = 0
upper_thresh = 40 # after extensive research, I am fairly certian that you only need to change this value...

Tk().withdraw()
filename = askopenfilename()
if filename.find(".jpg") == -1:
    # Load .png image
    image = cv2.imread(filename)

    # Save .jpg image
    cv2.imwrite('image.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    input_img = cv2.imread("image.jpg")
    facemap = facemesh.get_facemesh("image.jpg")

else:
    input_img = cv2.imread(filename)
    facemap = facemesh.get_facemesh(filename)

gray = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (blur_radius, blur_radius), 0)


edges = cv2.Canny(blur,lower_thresh,upper_thresh)

kernel = np.ones((3,3), np.uint8)

new_edges = cv2.dilate(edges, kernel, iterations=1)
new_edges = cv2.erode(new_edges, kernel, iterations=1)

cv2.imshow("source", input_img)
cv2.imshow("result", edges)
cv2.imshow("new result", new_edges)
cv2.waitKey(0)