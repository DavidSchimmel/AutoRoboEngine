import math
import numpy as np
import queue
import random

class Controller:
    def __init__(self, speed_normalizer, number_of_sensors, velocity_queue_length):
        self.speed_normalizer    = speed_normalizer
        self.inner_layer_1_nodes = 6
        self.weights_0           = 2 * (np.random.rand(number_of_sensors + self.inner_layer_1_nodes + 1, self.inner_layer_1_nodes) - 0.5) # initialize weights with random uniform distribution between -1 and 1
        self.weights_1           = 2 * (np.random.rand(self.inner_layer_1_nodes, 2) - 0.5) # initialize weights with random uniform distribution between -1 and 1
        self.velocity_queue      = queue.SimpleQueue()

        for i in range(velocity_queue_length):
            self.velocity_queue.put(np.zeros(self.inner_layer_1_nodes))
        pass

    def parse_input(self, sensors):
        parsed_input = np.zeros(len(sensors) + 2 + 1)
        for i in range(len(sensors)):
            parsed_input[i] = (sensors[i].length/sensors[i].range - 0.5) * 2 # normalize between -1 and 1
        parsed_input[-1] = 1 # bias node
        # parsed input [-3] and [-2] is left blank for the initial state of the motors with velocity = 0
        return parsed_input

    def process(self, input, weights = None, velocity_queue = None):
        weights          = self.weights if weights == None else weights
        velocity_queue   = self.velocity_queue if velocity_queue == None else velocity_queue
        input_parsed     = self.parse_input(input)
        remembered_speed = self.velocity_queue.get()

        for i in range(np.size(remembered_speed)):
            input_parsed[-1-i] = remembered_speed[i]

        output = self.feed_forward(input_parsed, weights)

        return output

    def feed_forward(self, input, weights_0, weights_1):
        z_1 = np.dot(input, weights_0)

        layer_1 = np.exp(z_1)
        layer_1 = layer_1/layer_1.sum()

        self.velocity_queue.put(layer_1)

        temp = layer_1.sum()

        z_2 = np.dot(layer_1, weights_1)


        output_1 = ((1/(1 + math.exp(-1*z_2[0]))) - 0.5) * 2
        output_2 = ((1/(1 + math.exp(-1*z_2[1]))) - 0.5) * 2
        return [output_1, output_2]

