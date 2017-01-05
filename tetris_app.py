#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# NOTE FOR WINDOWS USERS:
# You can download a "exefied" version of this game at:
# http://kch42.de/progs/tetris_py_exefied.zip
# If a DLL is missing or something like this, write an E-Mail (kevin@kch42.de)
# or leave a comment on this gist.

# Very simple tetris implementation
#
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!

# Copyright (c) 2010 "Kevin Chabowski"<kevin@kch42.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pygame
from board import Board
from controller import Controller
from constants import *
import sys
import inspect


class TetrisApp:
    def __init__(self):
        # Screen size and pygame parameter initialization
        pygame.init()
        pygame.key.set_repeat(250, 25)
        self.width = cell_size * (cols+6)
        self.height = cell_size * rows
        self.rlim = cell_size * cols
        self.bground_grid = [[8 if x % 2 == y % 2 else 0 for x in xrange(cols)] for y in xrange(rows)]
        self.default_font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)  # We do not need mouse movement events, so we block them.
        self.controller = Controller(self)
        self.board = Board(self)
        self.__init_game()

    def __init_game(self):
        self.board = Board(self)
        self.level = 1
        self.score = 0
        self.lines = 0
        self.gameover = False
        self.paused = False
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    def __disp_msg(self, msg, topleft):  # STAY
        x, y = topleft
        for line in msg.splitlines():
            self.screen.blit(self.default_font.render(line, False, (255, 255, 255), (0, 0, 0)), (x, y))
            y += 14

    def __center_msg(self, msg):   # STAY
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.default_font.render(line, False, (255, 255, 255), (0, 0, 0))
            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
            self.screen.blit(msg_image, (self.width // 2-msgim_center_x, self.height // 2-msgim_center_y+i*22))

    def draw_matrix(self, matrix, offset):  # STAY
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen,
                                     colors[val],
                                     pygame.Rect((off_x+x)*cell_size, (off_y+y) * cell_size, cell_size, cell_size), 0)

    def add_cl_lines(self, n): # TO NEW CLASS SCORING SYSTEM
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)

    def quit(self):
        self.__center_msg("Exiting...")
        pygame.display.update()
        sys.extone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.__init_game()
            self.gameover = False

    def run(self):
        self.gameover = False
        self.paused = False

        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.screen.fill((0, 0, 0))
            if self.gameover:
                self.__center_msg("""Game Over!\nYour score: %d. Press space to continue""" % self.score)
            else:
                if self.paused:
                    self.__center_msg("Paused")
                else:
                    pygame.draw.line(self.screen, (255, 255, 255), (self.rlim+1, 0), (self.rlim+1, self.height-1))
                    self.__disp_msg("Next:", (self.rlim+cell_size, 2))
                    self.__disp_msg("Score: %d\n\nLevel: %d\nLines: %d" % (self.score, self.level, self.lines), (self.rlim + cell_size, cell_size*5))
                    self.draw_matrix(self.bground_grid, (0, 0))
                    self.draw_matrix(self.board[:], (0, 0))
                    self.draw_matrix(self.board.playing_stone[:], (self.board.playing_stone.x, self.board.playing_stone.y))
            pygame.display.update()

            self.controller.process_events(pygame.event.get())

            dont_burn_my_cpu.tick(maxfps)

if __name__ == '__main__':
    App = TetrisApp()
    App.run()
