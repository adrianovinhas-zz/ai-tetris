from constants import *
from stone import StoneFactory
from copy import copy


class Board(object):
    def __init__(self, tetris_app):
        self.board = [[0 for x in xrange(cols)] for y in xrange(rows)]
        self.board_ids = [y for y in xrange(rows)]
        self.app = tetris_app
        self.stone_factory = StoneFactory()
        self.playing_stone = self.stone_factory.generate_stone()
        self.next_stone = self.stone_factory.generate_stone()

    def merge_stone(self, stone):
        for cy, row in enumerate(stone):
            for cx, val in enumerate(row):
                self.board[cy+stone.y-1][cx+stone.x] += val

    def remove_row(self, id_list):
        for row in id_list:
            del self.board[row]
            self.board = [[0 for i in xrange(cols)]] + self.board

    def new_stone(self):
        self.playing_stone = copy(self.next_stone)
        self.next_stone = self.stone_factory.generate_stone()
        if self.__check_collision(self.playing_stone, (self.playing_stone.x, self.playing_stone.y)):
            self.app.gameover = True

    def move_stone(self, delta_x):
        if not self.app.gameover and not self.app.paused:
            new_x = self.playing_stone.x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - self.playing_stone.width:
                new_x = cols - self.playing_stone.width
            if not self.__check_collision(self.playing_stone, (new_x, self.playing_stone.y)):
                self.playing_stone.x = new_x

    def drop_stone(self, manual):
        if not self.app.gameover and not self.app.paused:
            self.app.score += 1 if manual else 0
            self.playing_stone.y += 1
            if self.__check_collision(self.playing_stone, (self.playing_stone.x, self.playing_stone.y)):
                self.merge_stone(self.playing_stone)
                self.new_stone()
                cleared_rows = map(lambda x: x[1],
                                   filter(lambda x: 0 not in x[0], zip(self.board[:], self.board_ids)))
                self.remove_row(cleared_rows)
                self.app.add_cl_lines(len(cleared_rows))
                return True
        return False

    def insta_drop_stone(self):
        if not self.app.gameover and not self.app.paused:
            while not self.drop_stone(True):
                pass

    def rotate_stone(self):
        if not self.app.gameover and not self.app.paused:
            next_stone = self.playing_stone.rotate_clockwise()
            if not self.__check_collision(next_stone, (self.playing_stone.x, self.playing_stone.y)):
                print "test"
                print next_stone.shape
                self.playing_stone = next_stone

    def __check_collision(self, stone, offset):
        off_x, off_y = offset
        for cy, row in enumerate(stone[:]):
            for cx, cell in enumerate(row):
                try:
                    if cell and self.board[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False

    def __getitem__(self, key):
        return self.board[key]



