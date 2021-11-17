from cv2 import cv2
import numpy as np
import random as rd
import time
import math
import sys
import pickle
import facemesh

filename = "ricardo.jpg"
def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def distance(x1, y1, x2, y2):
    return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)

def middle_out(a, index):
    
    b = a[:]
    a_len = len(a)
    while b:
        yield b.pop(index * len(b) // len(a))

def spiral_out(x,y, spiral_radius):
    for j in range(1,spiral_radius+1):
        for i in range(x-j,x+j+1):
            yield (i,y+j)
            yield (i,y-j)
        for i in range(y-j+1, y+j):
            yield (x+j,i)
            yield (x-j,i)

def check_close(xP,yP):

    # for y in range(yP-20,yP+20):
    #     for x in range(xP-20, xP+20):
    #         if (x,y) == (xP, yP):
    #             continue
    #         if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
    #             if edges[y][x] == 255:
    #                 return(x,y)

    for x,y in spiral_out(xP,yP, 50):
        if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
            if edges[y][x] == 255:
                    return(x,y)

    return None

if filename.find(".jpg") == -1:
    # Load .png image
    image = cv2.imread(filename)

    # Save .jpg image
    cv2.imwrite('image.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    input_img = cv2.imread("image.jpg")
else:
    input_img = cv2.imread(filename)

facemap = facemesh.get_facemesh(filename)
gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (41, 41), 0)
cv2.imwrite("blurred.jpg", blur)
cv2.imwrite("facemesh.jpg", facemap)
# cv2.imwrite('edges.jpg',edges)

for y in range(len(blur)):
    for x in range(len(blur[y])):
        if facemap[x,y,0] == 0:
            blur[x, y] = gray[x,y]
            print(f"moved {x}, {y}")

blur = cv2.GaussianBlur(blur, (11, 11), 0)
edges = cv2.Canny(blur, 0, 25)
points = []
for y in range(len(edges)):
    for x in range(len(edges[y])):
        if edges[y][x] == 255:
            points.append((x,y))
sortedPoints = [points[0]]

len_points = len(points)

tt0 = time.time() 
for i in range(len_points-1):
    t0 = time.time()
    targetPoint = sortedPoints[i]

    if i % (len_points//200) == 0:

        print('\r', end="")
        print(f"{i/(len(points) + len(sortedPoints)) * 100: .2f}% complete", end = "")
    
    nearby = check_close(*targetPoint)

    if nearby is None:
        mindist = max(edges.shape[0:2])
        for j in points:
            dist = distance(targetPoint[0], targetPoint[1], j[0], j[1])
            if dist < mindist and j not in sortedPoints:
                mindist = dist
                nearby = j
                break

        

    sortedPoints.append(nearby)
    points.remove(nearby)
    edges[nearby[1]][nearby[0]] = 0
    
    
print("")
print(f"took {time.time()-tt0: .2f} seconds to sort all {len(sortedPoints)} points")
# filtered path = []
splitDistance = 4 # number of pixels apart when points are broken into seperate segments
angleCut = 40 # angle, lower == less agressive
distanceCut = 6 # pixels, higher == more agressive
minSegmentLen = 20 # minimum number of points (processed proir to angle and distance cuts) in a segment in order for it to be preserved

segments = []
index = 0
i = 0
while i < len(sortedPoints)-2:
    i+=1
    if distance(*(sortedPoints[i] + sortedPoints[i+1])) > splitDistance:
        segments.append(sortedPoints[index+1:i])
        index = i
segments.append(sortedPoints[index+1:])



i = 0
while i < len(segments)-2:
    i+=1
    if len(segments[i]) < minSegmentLen:
        segments.pop(i)
        i-=1


for seg in segments:
    i = 0
    while i < len(seg)-3:
        i+=1
        if 180 - angleCut < getAngle(seg[i], seg[i+1], seg[i+2]) < 180 + angleCut:
            seg.pop(i+1)
            i-=1
        


for seg in segments:
    i = 0
    while i < len(seg)-2:
        i+=1
        if distance(*(seg[i] + seg[i+1])) < distanceCut:
            seg.pop(i+1)
            i-=1




img = input_img.copy()
mask = cv2.inRange(img, (0,0,0), (255,255,255))
img[mask>0] = (255,255,255)
# img = cv2.imread('shrik2.png')

for seg in segments:

    color = tuple(rd.randrange(0,255) for i in range(3))
    # color = (0,0,0)

    i = 0
    for i in range(len(seg)-1):

        # print(seg[i])
        if distance(seg[i][0], seg[i][1], seg[i+1][0], seg[i+1][1]) < 2000:
            x1,y1,x2,y2 = seg[i][0], seg[i][1], seg[i+1][0], seg[i+1][1]
            cv2.line(img,(x1,y1),(x2,y2),color,2)

# print(len(points))
# print(len(lines))

i = 0
while i < len(segments):
    if len(segments[i]) <= 2:
        segments.pop(i)
        i-=1
    i+=1
# for i in range(len(segments)):

max_size = max(input_img.shape[:2])

for i, seg in enumerate(segments):
    for j, point in enumerate(seg):
        segments[i][j] = (point[0]/max_size,point[1]/max_size)


with open("path.pickle", 'wb') as file:
    pickle.dump(segments, file)

# import os
# import sys


# with open(os.path.join(sys.path[0], "path.pickle"), "rb") as file:
#         segments = pickle.load(file)
#         print(segments)
    



print("{} segments with a total of {} points".format(len(segments), sum(len(seg) for seg in segments)))
cv2.imwrite('houghlines6.jpg', img)
cv2.imwrite('gray.jpg', gray)
cv2.imwrite("final.jpg", blur)


edges = cv2.Canny(gray,0,40)
display = np.concatenate((input_img, cv2.cvtColor(edges,cv2.COLOR_GRAY2RGB)), axis=1)
display = np.concatenate((display, img), axis=1)


cv2.imshow("images", display)
cv2.waitKey(0)








# from pynput.mouse import Button, Controller
# import keyboard
# mouse = Controller()


# while True:

#     while not keyboard.is_pressed('c'):
#         pass

#     initPos = mouse.position
#     print(initPos)

#     for seg in segments:
        
#         mouse.position = np.add(seg[0], initPos)
#         mouse.press(Button.left)
#         time.sleep(.006)

#         for pos in range(len(seg)):
            
#             if keyboard.is_pressed('q'):
#                 raise("exiting")

#             mouse.position = np.add(seg[pos], initPos)
#             time.sleep(.001)
            
#         # time.sleep(.005)
#         mouse.release(Button.left)
#         time.sleep(.005)