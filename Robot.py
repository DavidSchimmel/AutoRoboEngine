from pygame.draw import (circle, aaline)
import math

class Robot:
    def __init__(self, config, pygame, display, colour, position, angle_degree = 90, size = 10):
        self.LEFT = "left"
        self.RIGHT = "right"

        self.config         = config

        self.game           = pygame
        self.display        = display

        self.velocity_left  = 0
        self.velocity_right = 0
        self.angle          = math.radians(angle_degree)
        self.position       = position
        self.colour         = colour
        self.size           = size

        self.draw_explicit(self.game, self.display, self.colour, self.position, self.size, self.angle)

    def draw_explicit(self, pygame, display, colour, position, size, angle):
        # draw robot body as circle
        pygame.draw.circle(display, colour, position, size)

        # draw direction indicator
        face = self.get_orientation_vector(angle, size)
        direction_vector = [position[0] + face[0], position[1] + face[1]]
        pygame.draw.aaline(display, (123, 12, 12), position, direction_vector)

        return

    def draw(self):
        self.draw_explicit(self.game, self.display, self.colour, self.position, self.size, self.angle)

    def get_orientation_vector(self, angle_radians, size_factor):
        orientation_normalized = (math.cos(angle_radians), math.sin(angle_radians))
        orientation_vector = [orientation_normalized[0] * size_factor, orientation_normalized[1] * size_factor]

        return orientation_vector

    def move(self):
        # wheel_distance = self.size / 2
        delta_t = 1

        if self.velocity_left == self.velocity_right:
            orientation = self.get_orientation_vector(self.angle, 1)
            velocity = (self.velocity_right + self.velocity_left) / 2
            self.position[0] = self.position[0] + velocity * orientation[0] * delta_t
            self.position[1] = self.position[1] + velocity * orientation[1] * delta_t
            return self.position

        omega = (self.velocity_right - self.velocity_left) / self.size
        R = (self.size / 2) * (self.velocity_right + self.velocity_left) / (self.velocity_right - self.velocity_left)

        ICC_x = self.position[0] - R * math.sin(self.angle)
        ICC_y = self.position[1] + R * math.cos(self.angle)

        x_updated  = math.cos(omega * delta_t) * (self.position[0] - ICC_x) - math.sin(omega * delta_t) * (self.position[1] - ICC_y) + ICC_x
        y_updated  = math.sin(omega * delta_t) * (self.position[0] - ICC_x) + math.cos(omega * delta_t) * (self.position[1] - ICC_y) + ICC_y

        self.angle = self.angle + omega * delta_t
        self.update_position(x_updated, y_updated)

        return self.position

    def update_position(self, x, y):
        self.position[0] = x
        self.position[1] = y
        return self.position

    def rotate_by_degree(self, angle_degree):
        self.angle = self.angle + angle_degree * 180 / math.pi
        return self.angle

    def acellarate(self, side, increment):
        if side   == self.LEFT:
            self.velocity_left  += self.config.ACCELERATION * increment
        elif side == self.RIGHT:
            self.velocity_right += self.config.ACCELERATION * increment
        return [self.velocity_left, self.velocity_right]

    def stop(self, sides = ["left", "right"]):
        for side in sides:
            if side == self.LEFT:
                self.velocity_left = 0
            elif side == self.RIGHT:
                self.velocity_right = 0
        return [self.velocity_left, self.velocity_right]
