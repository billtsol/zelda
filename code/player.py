import pygame
from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.hitbox = self.rect.inflate(0, -26) # x , y

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 5

        # Collision
        self.obstacle_sprites = obstacle_sprites

    def input(self): # key input
        keys = pygame.key.get_pressed() # get all keys pressed

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else :
            self.direction.y = 0


        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else :
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0: # you cannot normalize 0 vector
            self.direction = self.direction.normalize() # normalize vector to dicrease player speed

        self.hitbox.x += self.direction.x * speed # updating the x-coordinate of a rectangle's position
        self.collision('horizontal') # check horizontal collision

        self.hitbox.y += self.direction.y * speed # updating the y-coordinate of a rectangle's position
        self.collision('vertical') # check vertical collision

        self.rect.center = self.hitbox.center

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0 : # player moving right
                        self.hitbox.right = sprite.hitbox.left # move player right side to sprite left side

                    if self.direction.x < 0 : # player moving left
                        self.hitbox.left = sprite.hitbox.right # move player left side to sprite right side


        if direction == 'vertical':
             for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0 : # player moving down
                        self.hitbox.bottom = sprite.hitbox.top # move player bottom side to sprite top side

                    if self.direction.y < 0 : # player moving up
                        self.hitbox.top = sprite.hitbox.bottom # move player top side to sprite bottom side


    def update(self):
        self.input()
        self.move(self.speed)