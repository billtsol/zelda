import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)

        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement
        self.direction = pygame.math.Vector2()


    def move(self, speed):
        if self.direction.magnitude() != 0: # you cannot normalize 0 vector
            self.direction = self.direction.normalize() # normalize vector to dicrease player speed

        # updating the x-coordinate of a rectangle's position
        self.hitbox.x += self.direction.x * speed # type: ignore
        self.collision('horizontal') # check horizontal collision

        # updating the y-coordinate of a rectangle's position
        self.hitbox.y += self.direction.y * speed # type: ignore
        self.collision('vertical') # check vertical collision

        self.rect.center = self.hitbox.center # type: ignore

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites: # type: ignore
                if sprite.hitbox.colliderect(self.hitbox): # type: ignore
                    if self.direction.x > 0 : # player moving right
                        # move player right side to sprite left side
                        self.hitbox.right = sprite.hitbox.left # type: ignore

                    if self.direction.x < 0 : # player moving left
                        # move player left side to sprite right side
                        self.hitbox.left = sprite.hitbox.right # type: ignore


        if direction == 'vertical':
             for sprite in self.obstacle_sprites: # type: ignore
                if sprite.hitbox.colliderect(self.hitbox): # type: ignore
                    if self.direction.y > 0 : # player moving down
                        # move player bottom side to sprite top side
                        self.hitbox.bottom = sprite.hitbox.top # type: ignore

                    if self.direction.y < 0 : # player moving up
                        # move player top side to sprite bottom side
                        self.hitbox.top = sprite.hitbox.bottom # type: ignore
