seg = [(0,0), (1,0), (1,1)]

def distance(x1, y1, x2, y2):
    return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)



def calc_segment(seg, max_vel, max_accel, max_radius, frequency, john = "dumb"):

    # R = V^2/A

    max_radius = 0


    velocity = 0
    for a, b, c in zip(seg, seg[1:], seg[2:]):
        ab_dist = distance(*a, *b)
        bc_dist = distance(*b, *c)

        l = (max_accel * ab_dist - velocity ** 2) / (3 * max_accel) # math n shit
        r = ab_dist - l


        radius = min(radius, ab_dist/2, bc_dist/2)

def plot_path(points):
    import matplotlib.pyplot as plt
    plt.scatter(*zip(*points))
    plt.show()




if __name__ == "__main__":
    # print(calc_segment(seg, radius=))
    plot_path(seg)


