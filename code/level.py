import pygame
from settings import *
from tile import Tile
from player import Player
from support import import_csv_layout, import_folder
from random import choice

class Level:
    def __init__(self):

        # get the display serface
        self.display_serface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_LargeObjects.csv'),
        }

        graphics = {
            'grass' : import_folder('graphics/Grass'),
            'objects' : import_folder('graphics/objects')
        }

        for style,layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1': # if colums is not free space

                        x = col_index * TILESIZE # calculate x position
                        y = row_index * TILESIZE # calculate y position

                        if style == 'boundary':
                            Tile( (x,y), [ self.obstacle_sprites] , 'invisible') # remove visible_sprites group and make the boundaries invisible

                        if style == 'grass': # draw the grass
                            random_grass_image = choice(graphics['grass'])
                            Tile ( (x,y) , [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)

                        if style == 'object': # draw the objects
                            surface = graphics['objects'][int(col)]
                            Tile ( (x,y) , [self.visible_sprites, self.obstacle_sprites], 'object', surface)

        self.player = Player((2000, 1430), [self.visible_sprites],self.obstacle_sprites)


    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player) # draw the visible sprites
        self.visible_sprites.update()



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()

        self.display_serface = pygame.display.get_surface()

        self.half_width = self.display_serface.get_size()[0] // 2
        self.half_height = self.display_serface.get_size()[1] // 2

        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surface = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))


    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_serface.blit(self.floor_surface, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite : sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset

            self.display_serface.blit(sprite.image,offset_position)
