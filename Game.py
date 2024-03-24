import pygame as py
from var import *
from sys import *

class Game():
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((WIDTH,HEIGHT))
        self.clock = py.time.Clock()

        self.gameStateManager = GameStateManager('start')
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)

        self.states = {'start': self.start, 'level':self.level}
        
    def run(self):
        while True:

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    exit()
            
            if event.type == py.KEYDOWN:
                self.gameStateManager.set_state('level')

            self.states[self.gameStateManager.get_state()].run()

            py.display.update()
            self.clock.tick(FPS)

class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        keys= py.key.get_pressed()
        self.display.fill(COLOR['almond'])
        if keys[py.K_DOWN]:
            self.gameStateManager.set_state('start')

class Start():
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        self.display.fill(COLOR['sandy'])
        keys= py.key.get_pressed()
        if keys[py.K_UP]:
            self.gameStateManager.set_state('level')


class GameStateManager():
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

        

# aimporter dans le main
#if __name__=='__main__':
game = Game()
game.run()
                                        
  
        