#!/usr/bin/python
#-*- coding: utf-8 -*-
import random

from card import Card
from neuralnet import NeuralNetwork
from suit import Suit


def generateDispensableCard(seed=None):
    if seed is not None:
        random.seed(seed)
    card = Card()
    card.setSuit(Suit(random.randint(1, 5)))
    card.setValue(random.randint(1, 4))  # 5s are indispensable
    graveyard = [random.randint(0, 1) for i in range(25)]  # 0 if some corresponding cards are left else 1
    graveyard[int(card) - 1] = 0
    graveyard += card.toBinary()
    return graveyard


def generateIndispensableCard(seed=None):
    if seed is not None:
        random.seed(seed)
    card = Card()
    card.setSuit(Suit(random.randint(1, 5)))
    card.setValue(random.randint(1, 5))
    graveyard = [random.randint(0, 1) for i in range(25)]  # 0 if some corresponding cards are left else 1

    for i in range((Suit.toInt(card.getSuit()) - 1) * 5, int(card) - 1):  # none of the cards with same suit and lower value as the current card should have all of their identical cards discarded
        graveyard[i] = 0
    graveyard[int(card) - 1] = 1  # This one means that all the cards identical to the current card have been discarded but not the current card, which is necessary but not in keeping with the other slots
    graveyard += card.toBinary()
    return graveyard


if __name__ == '__main__':
    for i in range(10):
        seed = random.randint(-65536, 65535)
        random.seed(seed)
        nn = NeuralNetwork(neuronsPerLayer=[31, 31, 1], learningStep=0.1)
        kb = []
        testKB = []
        for i in range(10000):
            kb.append((generateDispensableCard(), [1]))
            kb.append((generateIndispensableCard(), [0]))

        for i in range(1000):
            testKB.append((generateDispensableCard(), [1]))
            testKB.append((generateIndispensableCard(), [0]))

        untrainedErrorOnKB = nn.test(knowledgeBase=kb)
        untrainedErrorOnTest = nn.test(knowledgeBase=testKB)
        trainedErrorOnKB1 = nn.train(knowledgeBase=kb)
        for _ in range(1000):
            nn.train(knowledgeBase=kb, doTests=False)
        trainedErrorOnKB1000 = nn.test(knowledgeBase=kb)
        trainedErrorOnTest = nn.test(knowledgeBase=testKB)

        print("untrainedErrorOnKB : ", untrainedErrorOnKB)
        print("untrainedErrorOnTest : ", untrainedErrorOnTest)
        print("trainedErrorOnKB1 : ", trainedErrorOnKB1)
        print("trainedErrorOnKB1000 : ", trainedErrorOnKB1000)
        print("trainedErrorOnTest : ", trainedErrorOnTest)
        print("seed : ", seed)
        print()
