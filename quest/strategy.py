from random import random
from math import tau, sin, cos

class Strategy:
    """Strategy
    """
    def choose_course(self, sprite, game):
        return (0, 0)

class RandomWalk(Strategy):
    """ A strategy which has the sprite walk randomly, with some chance 
    of changing direction
    """
    def __init__(self, change_prob=0.1):
        self.change_prob = change_prob
        self.set_random_direction()

    def choose_course(self, sprite, game):
        if random() < self.change_prob:
            self.set_random_direction()
        return (self.x, self.y)

    def set_random_direction(self):
        r = random() * tau
        self.x = cos(r)
        self.y = sin(r)

class DividedStrategy(Strategy):
    """One or the other, MDP
    """

    def __init__(self, strategy_a, strategy_b, ab_prob, ba_prob):
        self.strategy_a = self.current_strategy = strategy_a
        self.strategy_b = strategy_b
        self.ab_prob = ab_prob
        self.ba_prob = ba_prob

    def apply(self, sprite):
        self.consider_switching_strategy()
        self.current_strategy.apply(sprite)

    def consider_switching_strategy(self):
        if self.current_strategy is self.strategy_a:
             if random() < self.ab_prob:
                self.current_strategy = self.strategy_b
        else:
            if random() < self.ba_prob:
                self.current_strategy = self.strategy_a
