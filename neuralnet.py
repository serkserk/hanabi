#!/usr/bin/python
#-*- coding: utf-8 -*-
import random
import math
import time


class NeuralNetwork:
    """ This class models a Neural Network.
        Attributes:
            - self.layers
            - connexions
    """

    def __init__(self, neuronsPerLayer=[4, 8, 1], learningStep=None):
        """ Constructor.
            Args:
                - neuronsPerLayer : an array containing the number of neurons for each layer
                - the learning step, or Nu.
        """
        self.nInputs = neuronsPerLayer[0]  # number of input neurons
        self.layers = []                   # this list contains the layers. Each layer is a list of values
        # this list contains the connexion layers. Each connexion layer is a list of values.
        self.connexions = []               # We can identify the neurons involved by the connexion's index.
        # This list contains the biases for each neuron. it corresponds perfectly self.layers,
        self.biases = []                   # i.e. self.biases[i][j] is the bias for self.layers[i][j]
        # the learning step, or Nu.
        if learningStep is None:
            self.step = [0.05 * 2 ** i for i in range(len(neuronsPerLayer))]  # each layer has a learning step of 0.05*2^i => layer 1 = 0.1, layer 2 = 0.2 etc. Layer 0 has 0.05 but we don't care about it
        else:
            self.step = learningStep

        for layer in neuronsPerLayer:  # initializing neuron self.layers with zeroes
            self.layers.append([])
            for _ in range(layer):
                self.layers[-1].append(0)

        for i in range(len(self.layers) - 1):  # initializing connexions with random real values [-10, 10]
            self.connexions.append([])
            for _ in range(len(self.layers[i]) * len(self.layers[i + 1])):
                self.connexions[i].append(random.random() * 2 - 1)
            # the connexion from self.layers[i][j] to self.layers[i-1][k] is self.connexions[i-1][k*len(self.layers[i])+j]
            # the connexion from self.layers[i][j] to self.layers[i+1][k] is self.connexions[i][j*len(self.layers[i+1])+k]
            # the neurons corresponding to self.connexions[i][j] are self.layers[i][j/len(self.layers[i+1])] and self.layers[i+1][j%len(self.layers[i+1])]

        self.biases.append(None)  # self.biases[0] corresponds to self.layers[0] which is the input layer ; however inputs do not have biases.
        for i in range(1, len(neuronsPerLayer)):  # initializing bias layers with random real values [-10, 10]
            self.biases.append([])
            for _ in range(neuronsPerLayer[i]):
                self.biases[i].append(random.random() * 2 - 1)

    def compute(self, input):
        """ Output value computation method.
            Args:
                - input : an array of values corresponding to the input values of the network
            Raises ValueError if input is not the same length as the number of input neurons in the network
        """
        if len(input) != self.nInputs:
            raise ValueError("Input list length does not match number of input neurons in network")

        self.layers[0] = input

        for i in range(1, len(self.layers)):  # for each layer except input layer
            for j in range(len(self.layers[i])):   # for each neuron
                netj = 0                      # this is the raw value of the neuron (before it's passed to the sigmoid)
                for k in range(len(self.layers[i - 1])):  # for each connexion of the current neuron to the neurons of the previous layer
                    netj += self.layers[i - 1][k] * self.connexions[i - 1][k * len(self.layers[i]) + j]  # netj += value * connexion
                netj += self.biases[i][j]
                self.layers[i][j] = sigmoid(netj)
        return self.layers[-1]

    def backprop(self, targetValues):
        """ Backwards propagation algorithm.
            This method should be called immediately after compute() : It uses the last computed value as the output to correct.
            Args :
                - targetValues : a list of values corresponding to what was expected of the output neurons.
                                Must be the same size as the number of output neurons.
        """
        outputLayer = self.layers[-1]
        if len(targetValues) != len(outputLayer):
            raise ValueError("Target list length does not match number of output neurons in network")

        errorSignals = []  # a list of lists that contains the error signal for each neuron
        for layer in self.layers:  # initializing errorSignals to zeroes
            a = [0 for neuron in layer]
            errorSignals.append(a)

        # Backprop on the last layer
        for k in range(len(targetValues)):
            # error signal dk = (Tk-Ok) f'(Netk) = (Tk-Ok) f(Netk) (1-f(Netk)) = (Tk-Ok) Ok (1-Ok)
            dk = (targetValues[k] - outputLayer[k]) * outputLayer[k] * (1 - outputLayer[k])
            errorSignals[-1][k] = dk
            for j in range(len(self.layers[-2])):  # for each neuron in the second-to-last layer
                # connexion from current neuron of the second-to-last layer to current output neuron
                WjkOld = self.connexions[len(self.layers) - 2][j * len(self.layers[-1]) + k]
                WjkNew = WjkOld + self.step[-1] * dk * self.layers[-2][j]  # Wjk_old + Nu * Dk * Oj  with Nu depending on the current layer
                self.connexions[len(self.layers) - 2][j * len(self.layers[-1]) + k] = WjkNew

        # backprop on the rest of the network
        for i in range(len(self.layers) - 2, -1, -1):  # for each layer from the second-to-last to the first (the last computed index being 0 since -1 is excluded)
            for j in range(len(self.layers[i])):  # for each neuron
                for k in range(len(self.layers[i + 1])):
                    # update connexion
                    WhzOld = self.connexions[i][j * len(self.layers[i + 1]) + k]
                    dk = errorSignals[i + 1][k]
                    WhzNew = WhzOld + self.step[i] * dk * self.layers[i][j]
                    self.connexions[i][j * len(self.layers[i + 1]) + k] = WhzNew

                    # determine error signal for current neuron
                    oh = self.layers[i][j]
                    Whz = self.connexions[i][j * len(self.layers[i + 1]) + k]
                    dh = oh * (1 - oh) * Whz * errorSignals[i + 1][k]
                    errorSignals[i][j] += dh

    def getOutput(self):
        """
        Return the network's output value
        """
        return self.layers[-1]

    def train(self, knowledgeBase, doTests=True):
        """
        Train the neural network
        Args:
            -knowledgeBase: input for the neural network.
        """
        for example, expectedValues in knowledgeBase:
            # t1 = time.time()
            self.compute(example)
            # t2 = time.time()
            # print("compute: ", t2 - t1)
            self.backprop(expectedValues)
            # print("backprop: ", time.time() - t2)
        if doTests:
            return self.test(knowledgeBase)

    def test(self, knowledgeBase):
        from statistics import mean
        errors = [[] for _ in self.getOutput()]
        for example, expectedValues in knowledgeBase:
            self.compute(example)
            for i in range(len(expectedValues)):
                output = 0 if self.getOutput()[i] < 0.5 else 1
                errors[i].append(abs(expectedValues[i] - output))
        errors = [mean(l) for l in errors]
        return errors


def sigmoid(x):
    """ The sigmoid function
    """
    return 1 / (1 + math.exp(-x))
