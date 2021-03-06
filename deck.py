#!/usr/bin/python
#-*- coding: utf-8 -*-
import random
from suit import *
from card import *


class Deck:
    """
    Deck of the Hanabi game.
    """

    N_SHUFFLES = 100

    def __init__(self):
        self.deck = []
        suits = [Suit.white, Suit.red, Suit.blue, Suit.green, Suit.yellow]

        # creating the deck with 3 ones, 2 2s, 3s & 4s and 1 5 for each suit
        for s in suits:
            for i in range(3):
                self.deck.append(Card(s, 1))
            for i in range(2, 5):
                for j in range(2):
                    self.deck.append(Card(s, i))
            self.deck.append(Card(s, 5))

    def shuffle(self):
        random.shuffle(self.deck)

    def sort(self):
        self.deck.sort()

    def draw(self):
        if not self.empty():
            return self.deck.pop()

    def display(self):
        for i in self.deck:
            print(i.toString())

    def empty(self):
        return len(self.deck) <= 0

    def cardsLeft(self):
        return len(self.deck)

    def __len__(self):
        return len(self.deck)

    def __getitem__(self, key):
        return self.deck[key]
