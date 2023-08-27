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

        # sound
        main_sound = pygame.mixer.Sound('../audio/main.ogg')
        main_sound.set_volume(0.13)
        main_sound.play(loops = -1)

    def run(self):
        while True:
            if self.level.player.health <= 0:
                self.level = Level()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quit
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run() # run level
            pygame.display.update() # update the screen
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()