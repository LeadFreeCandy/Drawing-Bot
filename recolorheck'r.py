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

lines = np.zeros((len(input_img), len(input_img[1])), np.uint8)
for x in range(len(input_img)):
    for y in range(len(input_img[1])):
        good = True
        for i in range(3):
            if input_img[x][y][i] > 100:
                good = False
        if good:
            lines[x][y] = 255


cv2.imshow("source", input_img)
cv2.imshow("result", lines)
cv2.waitKey(0)