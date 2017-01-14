from abc import ABCMeta, abstractmethod
import pygame


class Controller(object):
    __metaclass__ = ABCMeta

    def __init__(self, tetris_app):
        self.app = tetris_app

    @abstractmethod
    def process_events(self): pass


class AIController(Controller):
    """Class that describes is listening for controls and takes actions over them"""

    def __init__(self, tetris_app):
        super(AIController, self).__init__(tetris_app)
        self.key_actions = {
            'LEFT': lambda: self.app.board.move_stone(-1),
            'RIGHT': lambda: self.app.board.move_stone(+1),
            'DROP': lambda: self.app.board.drop_stone(True),
            'ROTATE': lambda: self.app.board.rotate_stone()
            #'RETURN': lambda: self.app.board.insta_drop_stone()
        }

    def process_events(self, events):
        #for event in events:
        pass

class GUIController(Controller):
    """Class that describes is listening for controls and takes actions over them"""

    def __init__(self, tetris_app):
        super(GUIController, self).__init__(tetris_app)
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


class ControllerFactory:
    """
    """
    @staticmethod
    def create_controller(self, ai_enabled, gui_enabled, tetris_app, controller):
        if controller is "guicontroller" and gui_enabled is False:
            print "nao"
        elif controller is not "guicontroller" and ai_enabled is False:
            print "nao"

        if controller is "guicontroller":
            return GUIController(tetris_app)
        elif controller is "ai-controller":
            return AIController(tetris_app)
        else:
            print "nao"







