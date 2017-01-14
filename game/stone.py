from constants import *
from copy import deepcopy
from random import choice
import re, sys, inspect



class Stone(object):
    """Class that describes a generic Tetris stone played on the board"""

    shape = None
#TODO: Create angle attribute
    def __init__(self, copy=None):
        if copy is None:
            self.width = self.__get_width()  # The array is 2D. We grab one of them and take its length
            self.height = self.__get_height()
            self.x = int(cols / 2 - self.width/2)
            self.y = 0
        else:
            self.x = copy.x
            self.y = copy.y
            self.width = copy.width  # The array is 2D. We grab one of them and take its length
            self.height = copy.height

    def __get_width(self):
        """Returns the width of a stone"""
        return len(self.shape[0])

    def __get_height(self):
        """Returns the height of a stone"""
        return len(self.shape)

    def __getitem__(self, key):
        return self.shape[key]

    def rotate_clockwise(self):
        """Returns a new Stone instance which was rotated 90 degrees clockwise

        It uses the copy constructor to create a new Stone instance which is a copy of the old one and then changes its
        attributes, rotating its shape and recalculating the new stone's width and height based on the new shape.
        """
        new_stone = deepcopy(self)
        new_stone.shape = [[new_stone.shape[y][x]
                           for y in xrange(new_stone.height)]
                           for x in xrange(new_stone.width - 1, -1, -1)]
        new_stone.width = new_stone.__get_width()
        new_stone.height = new_stone.__get_height()
        return new_stone


class IStone(Stone):
    """Concrete implementation of one of the Tetris stones

    Shape:
    # # # #
    """
    def __init__(self):
        self.shape = [[6, 6, 6, 6]]
        super(IStone, self).__init__()


class JStone(Stone):
    """Concrete implementation of one of the Tetris stones

    Shape:
    #
    # # #
    """
    def __init__(self):
        self.shape = [[4, 0, 0],
                      [4, 4, 4]]
        super(JStone, self).__init__()


class LStone(Stone):
    """Concrete implementation of one of the Tetris stones

    Shape:
    # # #
    #
    """
    def __init__(self):
        self.shape = [[0, 0, 5],
                      [5, 5, 5]]
        super(LStone, self).__init__()


class OStone(Stone):
    """Concrete implementation of one of the Tetris stones

    Shape:
    # #
    # #
    """
    def __init__(self):
        self.shape = [[7, 7],
                      [7, 7]]
        super(OStone, self).__init__()


class SStone(Stone):
    """Concrete implementation of one of the Tetris stones

    Shape:
      # #
    # #
    """
    def __init__(self):
        self.shape = [[0, 2, 2],
                      [2, 2, 0]]
        super(SStone, self).__init__()


class TStone(Stone):
    """Concrete implementation of one of the Tetris stones

    Shape:
    # # #
      #
    """
    def __init__(self):
        self.shape = [[1, 1, 1],
                      [0, 1, 0]]
        super(TStone, self).__init__()


class ZStone(Stone):
    """Concrete implementation of one of the Tetris stones

    Shape:
    # #
      # #
    """
    def __init__(self):
        self.shape = [[3, 3, 0],
                      [0, 3, 3]]
        super(ZStone, self).__init__()


class StoneFactory:
    """
    """
    @staticmethod
    def generate_stone():
        stones = []
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if re.match(r"(.)*stone\.(.)+Stone(.)*", str(obj)):
                stones.append(name)
        return getattr(sys.modules[__name__], choice(stones))()