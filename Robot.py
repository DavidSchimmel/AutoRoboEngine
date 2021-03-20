#Simone and David
from pygame.draw import (circle, aaline)
import math
from collision_managment import resolve_collision
from Sensor import Sensor
from Controller import Controller
from Controller_2 import Controller_2
from Controller_3 import Controller_3

class Robot:
    def __init__(self, config, pygame, display, display_size, environment, colour, position, angle_degree, size, max_velocity, controller_weights):
        self.LEFT = "left"
        self.RIGHT = "right"

        self.config              = config

        self.game                = pygame
        self.display             = display
        self.environment         = environment
        self.environment_size    = display_size

        self.controller_weights  = controller_weights
        self.controller          = Controller_3(config.MAX_SPEED, self.config.SENSOR_COUNT, self.config.VELOCITY_QUEUE_LENGTH, self.controller_weights)
        # self.controller          = Controller(config.MAX_SPEED, self.config.SENSOR_COUNT, self.config.VELOCITY_QUEUE_LENGTH, self.controller_weights)

        self.velocity_left       = 0
        self.velocity_right      = 0
        self.max_velocity        = max_velocity
        self.angle               = math.radians(angle_degree)
        self.position            = position
        self.colour              = colour
        self.size                = size

        self.sensors = self.initialize_sensors(self.config.SENSOR_COUNT, angle_degree, self.config.SENSOR_RANGE, self.config.SENSOR_COLOUR, environment)
        self.check_sensors()

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
        if self.config.DEBUG:
            self.draw_sensors()

    def get_orientation_vector(self, angle_radians, size_factor):
        orientation_normalized = (math.cos(angle_radians), math.sin(angle_radians))
        orientation_vector = [orientation_normalized[0] * size_factor, orientation_normalized[1] * size_factor]

        return orientation_vector

    def move(self):
        col_detected=False
        delta_t = 1
        microstep = 0.05
        if self.velocity_left == self.velocity_right:
            orientation = self.get_orientation_vector(self.angle, 1)
            velocity = (self.velocity_right + self.velocity_left) / 2
            x_updated = self.position[0] + velocity * orientation[0] * delta_t
            y_updated = self.position[1] + velocity * orientation[1] * delta_t
            if(resolve_collision((self.position[0], self.position[1]),(x_updated, y_updated), self.size, self.environment, self.environment_size)):
                col_detected=True
                t=0
                x_updated = self.position[0]
                y_updated = self.position[1]
                while(t<delta_t and not resolve_collision((x_updated, y_updated), (x_updated + velocity * orientation[0] * microstep, y_updated + velocity * orientation[1] * microstep), self.size, self.environment, self.environment_size)):
                    x_updated = x_updated + velocity * orientation[0] * microstep
                    y_updated = y_updated + velocity * orientation[1] * microstep
                    t+=microstep
                while(t<delta_t): #translation
                    if not resolve_collision((x_updated, y_updated), (x_updated + velocity * orientation[0] * microstep, y_updated), self.size, self.environment, self.environment_size):
                        x_updated=x_updated + velocity * orientation[0] * microstep
                    if not resolve_collision((x_updated, y_updated), (x_updated, y_updated + velocity * orientation[1] * microstep), self.size, self.environment, self.environment_size):
                        y_updated=y_updated + velocity * orientation[1] * microstep
                    t+=microstep

            self.update_position(x_updated, y_updated)

            return self.position, col_detected, velocity, 0

        omega = (self.velocity_right - self.velocity_left) / self.size
        R = (self.size / 2) * (self.velocity_right + self.velocity_left) / (self.velocity_right - self.velocity_left)

        ICC_x = self.position[0] - R * math.sin(self.angle)
        ICC_y = self.position[1] + R * math.cos(self.angle)

        x_updated  = math.cos(omega * delta_t) * (self.position[0] - ICC_x) - math.sin(omega * delta_t) * (self.position[1] - ICC_y) + ICC_x
        y_updated  = math.sin(omega * delta_t) * (self.position[0] - ICC_x) + math.cos(omega * delta_t) * (self.position[1] - ICC_y) + ICC_y

        velocity = (self.velocity_right + self.velocity_left) / 2
        rotation = omega * delta_t

        if(resolve_collision((self.position[0], self.position[1]), (x_updated, y_updated), self.size, self.environment, self.environment_size)):
            col_detected=True
            t=0
            angle = self.angle
            x_updated = self.position[0]
            y_updated = self.position[1]
            x_updated_  = math.cos(omega * microstep) * (x_updated - ICC_x) - math.sin(omega * microstep) * (y_updated - ICC_y) + ICC_x
            y_updated_  = math.sin(omega * microstep) * (x_updated - ICC_x) + math.cos(omega * microstep) * (y_updated - ICC_y) + ICC_y
            while(t<delta_t and not resolve_collision((x_updated, y_updated), (x_updated_, y_updated_ ), self.size, self.environment, self.environment_size)):
                x_updated=x_updated_
                y_updated=y_updated_
                x_updated_  = math.cos(omega * microstep) * (x_updated - ICC_x) - math.sin(omega * microstep) * (y_updated - ICC_y) + ICC_x
                y_updated_  = math.sin(omega * microstep) * (x_updated - ICC_x) + math.cos(omega * microstep) * (y_updated - ICC_y) + ICC_y
                ICC_x = x_updated - R * math.sin(angle)
                ICC_y = y_updated + R * math.cos(angle)
                angle = angle + omega * microstep
                t+=microstep
            self.angle=angle
            orientation = self.get_orientation_vector(self.angle, 1)
            velocity = (self.velocity_right + self.velocity_left) / 2
            while(t<delta_t): #translation
                if not resolve_collision((x_updated, y_updated), (x_updated + velocity * orientation[0] * microstep, y_updated), self.size, self.environment, self.environment_size):
                    x_updated=x_updated + velocity * orientation[0] * microstep
                if not resolve_collision((x_updated, y_updated), (x_updated, y_updated + velocity * orientation[1] * microstep), self.size, self.environment, self.environment_size):
                    y_updated=y_updated + velocity * orientation[1] * microstep
                t+=microstep

        self.update_position(x_updated, y_updated)
        self.rotate(rotation)

        return self.position, col_detected, velocity, rotation


    def update_position(self, x, y):
        self.position[0] = x
        self.position[1] = y

        for sensor in self.sensors:
            sensor.shift_to(self.position)

        return self.position

    def rotate(self, rotation):
        self.angle = self.angle + rotation

        for sensor in self.sensors:
            sensor.rotate(rotation)

        return self.angle

    def acellarate(self, side, increment):
        # TODO Check max speed if you use it
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

    def initialize_sensors(self, sensor_count, facing_angle_degree, sensor_range, sensor_colour, environment):
        spacing_degree = 360 / sensor_count
        sensors = []
        current_angle_degree = facing_angle_degree
        for _ in range(sensor_count):
            sensors.append(Sensor(self.position, self.size + 1, current_angle_degree, sensor_range, sensor_colour, environment))
            current_angle_degree = current_angle_degree + spacing_degree

        return sensors

    def check_sensors(self):
        for sensor in self.sensors:
            sensor.update(self.environment)
        return

    def draw_sensors(self):
        for sensor in self.sensors:
            colour = sensor.colour
            if (sensor.collision_detected):
                colour = (222, 70, 10)
            self.game.draw.aaline(self.display, colour, sensor.root_vector, sensor.direction_vector)

    def controller_process(self, controller = None):
        controller = self.controller if controller == None else controller

        controller_output = self.controller.process(self.sensors)

        if controller.output_kind == "relative":
            directions = self.controller.process(self.sensors)
            self.acellarate(self.LEFT,  directions[0])
            self.acellarate(self.RIGHT, directions[1])
        else:
            self.velocity_left  = self.max_velocity * controller_output[0]
            self.velocity_right = self.max_velocity * controller_output[1]
