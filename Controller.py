#David
import math
import numpy as np
import queue
import random

class Controller:
    def __init__(self, speed_normalizer, number_of_sensors, velocity_queue_length, weights_init):
        self.speed_normalizer = speed_normalizer
        self.weights          = weights_init #2 * (np.random.rand(number_of_sensors + 2 + 1, 2) - 0.5) # initialize weights with random uniform distribution between -1 and 1
        self.velocity_queue   = queue.SimpleQueue()
        self.output_kind      = "relative"

        for i in range(velocity_queue_length):
            self.velocity_queue.put([0, 0])
        pass

    def parse_input(self, sensors):
        parsed_input = np.zeros(len(sensors) + 2 + 1)
        for i in range(len(sensors)):
            parsed_input[i] = (sensors[i].length/sensors[i].range - 0.5) * 2 # normalize between -1 and 1
        parsed_input[-1] = 1 # bias node
        # parsed input [-3] and [-2] is left blank for the initial state of the motors with velocity = 0
        return parsed_input

    def process(self, input, weights = None, velocity_queue = None):
        weights        = self.weights if weights == None else weights[0] # TODO remove the wrapper? or is it for the layer indicator?
        velocity_queue = self.velocity_queue if velocity_queue == None else velocity_queue

        input_parsed = self.parse_input(input)

        remembered_speed = self.velocity_queue.get()
        input_parsed[-3] = remembered_speed[0]
        input_parsed[-2] = remembered_speed[1]

        output = self.feed_forward(input_parsed, weights)
        directions = [self.get_direction(output[0]), self.get_direction(output[1])]

        return directions

    def feed_forward(self, input, weights):
        z = np.dot(input, weights)

        output_1 = 1/(1 + math.exp(-1*z[0][0]))
        output_2 = 1/(1 + math.exp(-1*z[0][1]))

        self.velocity_queue.put([output_1, output_2])
        test = self.velocity_queue.qsize()
        return [output_1, output_2]

    def get_direction(self, standardized_output):
        if standardized_output <= 0.4: # TODO might need to  find a good trade off for these thresholds
            return -1
        elif standardized_output >= 0.6:
            return 1
        else:
             return 0

