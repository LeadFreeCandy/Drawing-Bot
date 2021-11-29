import numpy as np
import math

def sin(degrees):
    return math.sin(math.radians(degrees))

def cos(degrees):
    return sin(degrees+90)

def distance(x1, y1, x2, y2):
    return (((x2-x1) ** 2 + (y2 - y1) ** 2) ** .5)






class Line():

    def __init__(self, start_pos, end_pos, start_vel = None, acceleration = None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.start_vel = start_vel
        self.acceleration = acceleration
        pass
    
    def __repr__(self):

        return str(f"<Line from {self.start_pos} to {self.end_pos} {self.start_vel=} {self.acceleration=} {self.end_vel=}>")

    def get_len(self):
        return distance(*self.start_pos, *self.end_pos)


    @property
    def end_vel(self):
        if self.start_vel is not None:
            return math.sqrt(self.start_vel ** 2 + 2 * self.acceleration * self.get_len())
        else:
            return None

    def find_start_vel(self, accel, vf):
        try:
            return math.sqrt(vf ** 2 + 2 * accel * self.get_len())
        except ValueError:
            return 0
    def find_accel(self, vf):
        return (vf ** 2 - self.start_vel ** 2) / (2 * self.get_len())
    def set_end_vel(self, vel, max_accel):
        # if just modified accel, return None
        # if modified accel and start_vel, return start_vel

        # self.end_vel = vel
        min_start_vel = self.find_start_vel(max_accel, vel) # THIS BROKE
        # print(f"{max_accel=}")
        # print(f"{vel=}")
        # print(f"{self.end_vel=}")
        # print(f"{self.start_vel=}")
        # print(f"{min_start_vel=}")
        if min_start_vel > self.start_vel:
            self.acceleration = self.find_accel(vel)
            return None
        else:
            self.start_vel = min_start_vel
            self.acceleration = -max_accel
            return self.start_vel

    def get_points_crude(self, num_points):
        points = []
        
        if self.start_pos == self.end_pos:
            return [self.start_pos]
        elif self.start_pos[0] == self.end_pos[0]:
            x = self.start_pos[0]
            for y in np.arange(self.start_pos[1], self.end_pos[1], (self.end_pos[1]-self.start_pos[1])/num_points):
                points.append((x,y))
        elif self.start_pos[1] == self.end_pos[1]:
            y = self.start_pos[1]
            for x in np.arange(self.start_pos[0], self.end_pos[0], (self.end_pos[0]-self.start_pos[0])/num_points):
                points.append((x,y))
        else:
            for x,y in zip(np.arange(self.start_pos[0], self.end_pos[0], (self.end_pos[0]-self.start_pos[0])/num_points),
             np.arange(self.start_pos[1], self.end_pos[1], (self.end_pos[1]-self.start_pos[1])/num_points)):
                points.append((x,y))

        return points

class Arc():
    def __init__(self, center_pos, radius, start_angle, end_angle):
        self.center_pos = center_pos
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        pass

    def __repr__(self):
        return str(f"<Arc centered at {self.center_pos}, from {self.start_angle} to {self.end_angle} with radius {self.radius}>")

    def max_accel(self, vel):

        return vel ** 2 / self.radius

    def max_speed(self, accel):
        return math.sqrt(accel * self.radius)
    def get_points_crude(self, num_points):
       
        points = []

        if self.end_angle - self.start_angle < -180:
            self.end_angle += 360
        elif self.end_angle - self.start_angle > 180:
            self.end_angle -= 360

        for angle in np.arange(self.start_angle, self.end_angle, (self.end_angle-self.start_angle)/num_points):
            points.append((cos(angle) * self.radius + self.center_pos[0], sin(angle) * self.radius + self.center_pos[1]))
        return points


    # def get_max_speed()