from pygame.draw import (circle, aaline)
import math
from collision_managment import resolve_collision

class Robot:
    def __init__(self, config, pygame, display, colour, position, env, orientation = (0, -1), size = 10, display_size=(700,700)):
        self.LEFT = "left"
        self.RIGHT = "right"

        self.config         = config

        self.game           = pygame
        self.display        = display

        self.velocity_left  = 0
        self.velocity_right = 0
        self.orientation    = orientation
        self.position       = position
        self.colour         = colour
        self.size           = size

        self.draw_explicit(self.game, self.display, self.colour, self.position, self.size, self.orientation)
        
        self.env = env
        self.env_size = display_size

    def draw_explicit(self, pygame, display, colour, position, size, orientation):
        # draw robot body as circle
        pygame.draw.circle(display, colour, position, size)

        # draw direction indicator
        face_position = (position[0] + orientation[0] * size, position[1] + orientation[1] * size)
        pygame.draw.aaline(display, (123, 12, 12), position, face_position)
        return

    def draw(self):
        self.draw_explicit(self.game, self.display, self.colour, self.position, self.size, self.orientation)

    def move(self):
        # wheel_distance = self.size / 2
        delta_t = 1

        if self.velocity_left == self.velocity_right:
            velocity = (self.velocity_right + self.velocity_left) / 2
            self.position[0] = self.position[0] + velocity * self.orientation[0] * delta_t
            self.position[1] = self.position[1] + velocity * self.orientation[1] * delta_t

            self.position[0], self.position[1] = resolve_collision(self.position, (velocity * self.orientation[0], velocity * self.orientation[1]), self.size, self.env, self.env_size)
            return self.position


        orientation_normalizing_factor = math.sqrt(self.orientation[0] ** 2 + self.orientation[1] ** 2)
        angle = math.acos(self.orientation[0] / orientation_normalizing_factor) # normalization factor should be one, as the orientation vector should be normalized

        omega = (self.velocity_right - self.velocity_left) / self.size
        R = (self.size / 2) * (self.velocity_right + self.velocity_left) / (self.velocity_right - self.velocity_left)

        ICC_x = self.position[0] - R * math.sin(angle)
        ICC_y = self.position[1] + R + math.cos(angle)

        x_updated     = math.cos(omega * delta_t) * (self.position[0] - ICC_x) - math.sin(omega * delta_t) * (self.position[1] - ICC_y) + ICC_x
        y_updated     = math.sin(omega * delta_t) * (self.position[0] - ICC_x) + math.cos(omega * delta_t) * (self.position[1] - ICC_y) + ICC_y
        angle_updated = angle  + omega * delta_t

        self.update_position(x_updated, y_updated)
        self.rotate(angle_updated)

        velocity = (self.velocity_right + self.velocity_left) / 2
        self.position[0], self.position[1] = resolve_collision(self.position, (velocity * self.orientation[0], velocity * self.orientation[1]), self.size, self.env, self.env_size)

        return self.position

    def update_position(self, x, y):
        self.position[0] = x
        self.position[1] = y
        return self.position

    def rotate(self, angle):
        x_rotated = math.cos(angle * self.orientation[0]) - math.sin(angle * self.orientation[1])
        y_rotated = math.sin(angle * self.orientation[0]) + math.cos(angle * self.orientation[1])
        self.orientation = [x_rotated, y_rotated]
        return self.orientation

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
