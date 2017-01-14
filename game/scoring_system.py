from constants import *

class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class ScoringSystem(object):
    __metaclass__ = SingletonType

    def __init__(self):
        self.points = 0

    def score_lines(self, level, n):
        self.points += level * linescores[n]

    def add_extra_points(self, extra_points):
        self.points += extra_points

    def reset_score(self):
        self.points = 0
