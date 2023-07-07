import pygame
from settings import *
from tile import Tile
from player import Player


class Level:
    def __init__(self):

        # get the display serface
        self.display_serface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):

        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):

                x = col_index * TILESIZE # calculate x position
                y = row_index * TILESIZE # calculate y position

                if col == 'x': # draw rock
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])

                elif col == 'p': # draw player
                    self.player = Player((x,y), [self.visible_sprites],self.obstacle_sprites)


    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.display_serface) # draw the visible sprites
        self.visible_sprites.update()