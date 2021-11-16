import math
import numpy as np

seg = [(0,0), (1,0), (1,1), (2, 1)]

def distance(x1, y1, x2, y2):
    return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)

def parametric_arc(t: 0-1, starpos, endpos, radius):
    pass

def arc_points(startpos, endpos, num_poins):
    pass




def line_points(start_pos, end_pos, start_vel, end_vel, num_points):

    points = []

    if start_pos[0] == end_pos[0]:
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
    for a, b, c in zip(seg, seg[1:], seg[2:]):
        ab_dist = distance(*a, *b)
        bc_dist = distance(*b, *c)

        # l = (max_accel * ab_dist - velocity ** 2) / (3 * max_accel) # math n shit
        r = ab_dist - (max_accel * ab_dist - velocity ** 2) / (3 * max_accel)
        # vf = math.sqrt(velocity ** 2 + 2 * max_accel * l)

        r = min(r, ab_dist/2, bc_dist/2, max_radius)
        l = ab_dist-r

        vf = min(math.sqrt(velocity ** 2 + 2 * max_accel * l), math.sqrt(max_accel * r))
        assert velocity - max_accel *l <= vf, 'does not have time to slow'



        r2_max = bc_dist - r
        vf2_max = math.sqrt(max_accel * r2_max)

        if vf > vf2_max: #velocity limited
            raise "uh maybe dis code do be needed doe"
            vf = vf2_max
            l = (vf ** 2 - velocity ** 2) / (2 * max_accel)
            r = ab_dist - l


        velocity = vf


        # radius = min(radius, ab_dist/2, bc_dist/2)

        print(f"{r = }, {l = }, {vf = }")

        ratio = l/ab_dist
        end_pos = (a[0] * (1-ratio) + b[0] * ratio, a[1] * (1-ratio) + b[1] * ratio)

        points += line_points(a, end_pos, 0,0, 10)

    return points


def plot_path(points):
    import matplotlib.pyplot as plt
    plt.scatter(*zip(*points))
    plt.show()




if __name__ == "__main__":
    # print(calc_segment(seg, radius=))
    points = calc_segment(seg, 1, 1, .1, 1)
    plot_path(points)


