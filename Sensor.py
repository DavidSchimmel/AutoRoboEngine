#David
import math
from collision_managment import *

class Sensor:
    def __init__(self, anchor_position, anchor_distance, angle_degree, sensor_range, colour, environment):
        self.anchor_position    = anchor_position
        self.anchor_distance    = anchor_distance
        self.angle              = math.radians(angle_degree)
        self.range              = sensor_range
        self.colour             = colour
        self.root_vector        = []
        self.direction_vector   = []
        self.length             = sensor_range
        self.collision_detected = False

        self.update(environment)

        return

    def update(self, environment):
        self.update_explicit(self.anchor_position, self.anchor_distance, self.angle, self.range, environment)

    def update_explicit(self, anchor_position, anchor_distance, angle, sensor_range, environment):
        epsilon = 1
        orientation_normalized = (math.cos(angle), math.sin(angle))

        root_vector      = [orientation_normalized[0] * anchor_distance,                  orientation_normalized[1] * anchor_distance]
        direction_vector = [orientation_normalized[0] * (sensor_range + anchor_distance), orientation_normalized[1] * (sensor_range + anchor_distance)]

        # include error margin for very close obstacles
        epsilon_x_signum = -1 if root_vector[0] > 0 else 1
        epsilon_y_signum = -1 if root_vector[1] > 0 else 1
        root_vector[0] = root_vector[0] + (epsilon_x_signum * epsilon)
        root_vector[1] = root_vector[1] + (epsilon_y_signum * epsilon)
        direction_vector[0] = direction_vector[0] + (epsilon_x_signum * epsilon)
        direction_vector[1] = direction_vector[1] + (epsilon_y_signum * epsilon)

        self.root_vector      = [anchor_position[0] + root_vector[0],      anchor_position[1] + root_vector[1]]
        self.direction_vector = [anchor_position[0] + direction_vector[0], anchor_position[1] + direction_vector[1]]

        self.collision_detected = False
        intersections = find_intersection(self.root_vector, self.direction_vector, self.range, environment)
        if (len(intersections) > 0):
            self.direction_vector = self.find_closest_intersection(self.root_vector, intersections)
            self.collision_detected = True

        self.length = math.sqrt((self.direction_vector[1] - self.root_vector[1])**2 + (self.direction_vector[0] - self.root_vector[0])**2)

        return self.root_vector, self.direction_vector, self.collision_detected, self.length

    def shift_to(self, anchor_position):
        self.anchor_position = anchor_position

    def rotate(self, rotation):
        self.angle = self.angle + rotation

    def find_closest_intersection(self, root_vector, intersections):
        closest_intersection = intersections[0]
        smallest_distance = math.sqrt((intersections[0][1] - root_vector[1])**2 + (intersections[0][0] - root_vector[0])**2)
        for intersection in intersections:
            distance =      math.sqrt((intersection[1]     - root_vector[1])**2 + (intersection[0]     - root_vector[0])**2)
            if (distance < smallest_distance):
                smallest_distance = distance
                closest_intersection = intersection

        return closest_intersection

