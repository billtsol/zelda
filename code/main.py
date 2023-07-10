import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # set screen dimensions
        pygame.display.set_caption('Zelda') # set titleq
        self.clock = pygame.time.Clock()

        self.level = Level() # initialize level

    def run(self):
        while True:
            for event in pygame.event.get():
              if event.type == pygame.QUIT: # quit
                  pygame.quit()
                  sys.exit()

            self.screen.fill('black') # make the screen black

            self.level.run() # run level

            pygame.display.update() # update the screen
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()