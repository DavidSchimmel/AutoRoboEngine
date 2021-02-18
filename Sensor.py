import math

class Sensor:
    def __init__(self, anchor_position, anchor_distance, angle_degree, sensor_range, colour):
        self.anchor_position  = anchor_position
        self.anchor_distance  = anchor_distance
        self.angle            = math.radians(angle_degree)
        self.range            = sensor_range
        self.colour           = colour
        self.root_vector      = []
        self.direction_vector = []

        self.update()

        return



    def update(self):
        self.update_explicit(self.anchor_position, self.anchor_distance, self.angle, self.range)

    def update_explicit(self, anchor_position, anchor_distance, angle, sensor_range):
        orientation_normalized = (math.cos(angle), math.sin(angle))

        root_vector      = [orientation_normalized[0] * anchor_distance,                orientation_normalized[1] * anchor_distance]
        direction_vector = [orientation_normalized[0] * (sensor_range + anchor_distance), orientation_normalized[1] * (sensor_range + anchor_distance)]

        self.root_vector      = [anchor_position[0] + root_vector[0],      anchor_position[1] + root_vector[1]]
        self.direction_vector = [anchor_position[0] + direction_vector[0], anchor_position[1] + direction_vector[1]]

        return self.root_vector, self.direction_vector

    def shift_to(self, anchor_position):
        self.anchor_position = anchor_position

    def rotate(self, rotation):
        self.angle = self.angle + rotation

