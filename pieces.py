class Line():
    def __init__(self, start_pos, end_pos, start_vel = None, acceleration = None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        pass

class Arc():
    def __init__(self, center_pos, radius, start_angle):
        self.center_pos = center_pos
        self.radius = radius
        self.start_angle = start_angle
        pass