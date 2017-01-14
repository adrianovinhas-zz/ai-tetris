from abc import ABCMeta, abstractmethod


class ScoringSystem(object):
    __metaclass__ = ABCMeta

    _instance = None
    points = None

    def __init__(self, instance):
        if ScoringSystem._instance is None and points is None:
            ScoringSystem._instance = instance
            points = 0


    @abstractmethod
    def score_lines(self): pass
