from pygame.draw import (circle, aaline)

class Robot:
    def __init__(self, config, pygame, display, colour, position, orientation = (0, -1), size = 10):
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

    def draw_explicit(self, pygame, display, colour, position, size, orientation):
        # draw robot body as circle
        pygame.draw.circle(display, colour, position, size)

        # draw direction indicator
        face_position = (position[0] + orientation[0] * size, position[1] + orientation[1] * size)
        pygame.draw.aaline(display, (123, 12, 12), position, face_position)
        return

    def draw(self):
        self.draw_explicit(self.game, self.display, self.colour, self.position, self.size, self.orientation)

    def update_position(self):
        self.position[1] = self.position[1] + self.velocity_left + self.velocity_right
        return

    def update_orientation(self):
        return

    def acellarate(self, side):
        if side   == "left":
            self.velocity_left  += self.config.ACCELERATION * -1 # FIXME
        elif side == "right":
            self.velocity_right += self.config.ACCELERATION * -1 # FIXME