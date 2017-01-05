from constants import *
import pygame
import inspect


class Controller(object):
    """Class that describes is listening for controls and takes actions over them"""

    def __init__(self, tetris_app):
        self.app = tetris_app
        self.key_actions = {
            'ESCAPE': self.app.quit,
            'LEFT': lambda: self.app.board.move_stone(-1),
            'RIGHT': lambda: self.app.board.move_stone(+1),
            'DOWN': lambda: self.app.board.drop_stone(True),
            'UP': lambda: self.app.board.rotate_stone(),
            'p': self.app.toggle_pause,
            'SPACE': self.app.start_game,
            'RETURN': lambda: self.app.board.insta_drop_stone()
        }

    def process_events(self, events):
        for event in events:
            if event.type == pygame.USEREVENT+1:
                self.app.board.drop_stone(False)
            elif event.type == pygame.QUIT:
                self.app.quit()
            elif event.type == pygame.KEYDOWN:
                for key in self.key_actions:
                    if event.key == eval("pygame.K_"+key):
                        self.key_actions[key]()





