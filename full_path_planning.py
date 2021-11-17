import math
import numpy as np
from pieces import Line, Arc, sin, cos

seg = [(0,0), (0,1), (1,1), (1,0)]

def distance(x1, y1, x2, y2):
    return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)




def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang




def calc_segment(seg, max_accel, max_radius, john = "dumb"):

    # R = V^2/A

    points = []
    parts = []



    for i in range(len(seg)-2):
        a, b, c = seg[i:i+3]

        ab_dist = distance(*a, *b)
        bc_dist = distance(*b, *c)
        abc_angle = getAngle(a,b,c)

        if abc_angle == 180:
            l = ab_dist
            r = 0
            lr = 0
            
            parts.append(Line(a, b))
            
        else:
            # l = (max_accel * ab_dist - velocity ** 2) / (3 * max_accel) # math n shit

            lr = min(ab_dist, bc_dist/2) #TODO: decide if max radius should govrn lr or r
            r = (2 * sin(abc_angle/2) * lr) / abs(2 * sin(90-abc_angle/2))
            
            if r > max_radius:
                r = max_radius
                lr = (r * abs(2 * sin(90 - abc_angle/2)))/ (2 * sin(abc_angle/2))

            l = ab_dist - lr
            

            print(f"{r = }, {l = }")

            ratio = l/ab_dist
            end_pos = (a[0] * (1-ratio) + b[0] * ratio, a[1] * (1-ratio) + b[1] * ratio)

            ratio2 = lr/bc_dist
            new_pos = (b[0] * (1-ratio2) + c[0] * ratio2, b[1] * (1-ratio2) + c[1] * ratio2)

            seg[i+1] = new_pos

            # points += line_points(a, end_pos, 100)
            parts.append(Line(a, end_pos))



        shifter = (-(b[1]-a[1])/ab_dist * r, (b[0]-a[0])/ab_dist *r)
        circle_center = None
        if abc_angle > 180:
            circle_center = (end_pos[0]+shifter[0], end_pos[1]+shifter[1])
        elif abc_angle < 180:
            circle_center = (end_pos[0]-shifter[0], end_pos[1]-shifter[1])
        

        if circle_center:
            # points += [circle_center] # make sure axe dis shit
            circle_center_offset = (circle_center[0]+1, circle_center[1])
            # points += arc_points(circle_center, r, getAngle(circle_center_offset, circle_center, end_pos), getAngle(circle_center_offset, circle_center, new_pos), 100)
            parts.append(Arc(circle_center, r, getAngle(circle_center_offset, circle_center, end_pos), getAngle(circle_center_offset, circle_center, new_pos)))


    parts.append(Line(*seg[-2:]))


    
    
    # print(parts)
    return(parts)

def plot_path(parts):
    import matplotlib.pyplot as plt

    # x,y = zip(*points)
    points = []
    for chunk in parts:
        points += chunk.get_points_crude(100)

    x = [point[0] for point in points]

    plt.scatter(*zip(*points))
    plt.show()




if __name__ == "__main__":
    # print(calc_segment(seg, radius=))
    parts = calc_segment(seg, 1, 10)
    print(parts)
    plot_path(parts)


