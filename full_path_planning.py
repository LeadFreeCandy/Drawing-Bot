import math
import numpy as np

seg = [(0,1), (1,1), (2,0), (5,5)]

def distance(x1, y1, x2, y2):
    return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)



def arc_points(center_pos, radius, start_angle, end_angle, num_points):
    points = []

    if end_angle - start_angle < -180:
        end_angle += 360
    elif end_angle - start_angle > 180:
        end_angle -= 360

    for angle in np.arange(start_angle, end_angle, (end_angle-start_angle)/num_points):
        points.append((cos(angle) * radius + center_pos[0], sin(angle) * radius + center_pos[1]))
    return points
def sin(degrees):
    return math.sin(math.radians(degrees))

def cos(degrees):
    return sin(degrees+90)

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def line_points(start_pos, end_pos, num_points):

    points = []


    if start_pos == end_pos:
        return [start_pos]
    elif start_pos[0] == end_pos[0]:
        x = start_pos[0]
        for y in np.arange(start_pos[1], end_pos[1], (end_pos[1]-start_pos[1])/num_points):
            points.append((x,y))
    elif start_pos[1] == end_pos[1]:
        y = start_pos[1]
        for x in np.arange(start_pos[0], end_pos[0], (end_pos[0]-start_pos[0])/num_points):
            points.append((x,y))
    else:
        for x,y in zip(np.arange(start_pos[0], end_pos[0], (end_pos[0]-start_pos[0])/num_points), np.arange(start_pos[1], end_pos[1], (end_pos[1]-start_pos[1])/num_points)):
            points.append((x,y))

    return points


def calc_segment(seg, max_vel, max_accel, max_radius, frequency, john = "dumb"):

    # R = V^2/A

    points = []


    velocity = 0
    for i in range(len(seg)-2):
        a, b, c = seg[i:i+3]

        ab_dist = distance(*a, *b)
        bc_dist = distance(*b, *c)
        abc_angle = getAngle(a,b,c)

        # l = (max_accel * ab_dist - velocity ** 2) / (3 * max_accel) # math n shit

        lr = min(ab_dist, bc_dist/2) #TODO: decide if max radius should govrn lr or r
        r = (2 * sin(abc_angle/2) * lr) / abs(2 * sin(90-abc_angle/2))
        
        if r > max_radius:
            r = max_radius
            lr = (r * abs(2 * sin(90 - abc_angle/2)))/ (2 * sin(abc_angle/2))

        l = ab_dist - lr
        vf = min(math.sqrt(velocity ** 2 + 2 * max_accel * l), math.sqrt(max_accel * r))
        

        # assert velocity - max_accel *l <= vf, 'does not have time to slow'
        velocity = vf

        # r = ab_dist - (max_accel * ab_dist - velocity ** 2) / (3 * max_accel)
        # vf = math.sqrt(velocity ** 2 + 2 * max_accel * l)


        r2_max = bc_dist - r
        vf2_max = math.sqrt(max_accel * r2_max)

        # if vf > vf2_max: #velocity limited
        #     raise "uh maybe dis code do be needed doe"
        #     vf = vf2_max
        #     l = (vf ** 2 - velocity ** 2) / (2 * max_accel)
        #     r = ab_dist - l

        


        # radius = min(radius, ab_dist/2, bc_dist/2)

        print(f"{r = }, {l = }, {vf = }")

        ratio = l/ab_dist
        end_pos = (a[0] * (1-ratio) + b[0] * ratio, a[1] * (1-ratio) + b[1] * ratio)

        ratio2 = lr/bc_dist
        new_pos = (b[0] * (1-ratio2) + c[0] * ratio2, b[1] * (1-ratio2) + c[1] * ratio2)

        seg[i+1] = new_pos

        points += line_points(a, end_pos, 100)

        shifter = (-(b[1]-a[1])/ab_dist * r, (b[0]-a[0])/ab_dist *r)


        circle_center = None
        if abc_angle > 180:
            circle_center = (end_pos[0]+shifter[0], end_pos[1]+shifter[1])
        elif abc_angle < 180:
            circle_center = (end_pos[0]-shifter[0], end_pos[1]-shifter[1])
        else:
            raise "fuck"
        points += [circle_center]

        # points += line_points(end_pos, new_pos, 100)

        circle_center_offset = (circle_center[0]+1, circle_center[1])
        points += arc_points(circle_center, r, getAngle(circle_center_offset, circle_center, end_pos), getAngle(circle_center_offset, circle_center, new_pos), 100)

    points += line_points(*seg[-2:], 100) 
    
    return points


def plot_path(points):
    import matplotlib.pyplot as plt
    plt.scatter(*zip(*points))
    plt.show()




if __name__ == "__main__":
    # print(calc_segment(seg, radius=))
    points = calc_segment(seg, 1, 1, 1, 1)
    plot_path(points)


