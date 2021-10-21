import cv2
import time
import numpy as np

img = cv2.imread('test.jpg')

# cv2.imshow('Original', img) 
# cv2.waitKey(0)


img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.GaussianBlur(img_gray, (13,13), 0)



edges = cv2.Canny(image=img, threshold1=0, threshold2=0) # Canny Edge Detection

for i in range(10,150,10):
    
    edges = np.concatenate((edges, cv2.Canny(image=img, threshold1=0, threshold2=i)), axis=1) 

row = edges
for i in range(10,150,10):
    edges = cv2.Canny(image=img, threshold1=i, threshold2=0) # Canny Edge Detection
    
    for j in range(10,150,10):
        edges = np.concatenate((edges, cv2.Canny(image=img, threshold1=i, threshold2=j)), axis=1) 

    
    
    row = np.concatenate((row, edges), axis=0)

# edges = cv2.Canny(image=img, threshold1=100, threshold2=50) # Canny Edge Detection

# edges = np.concatenate((edges, edges), axis=1)

# Display Canny Edge Detection Image

# cv2.imshow('Canny Edge Detection', edges)

# cv2.waitKey(0)

cv2.imwrite("out.jpg", row)