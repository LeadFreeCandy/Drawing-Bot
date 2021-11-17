from cv2 import accumulate
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
        return str(f"<Line from {self.start_pos} to {self.end_pos} {self.start_vel=} {self.acceleration=}>")

    def get_len(self):
        return distance(self.start_pos, self.end_pos)

    def max_accel(self):
        return self.get_len() * self.acceleration

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