import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.hitbox = self.rect.inflate(0, -26) # x , y

        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = 0
        self.switch_duration_cooldown = 200

        # Collision
        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = 'graphics/player/'

        self.animations = {
            'up' : [], 'down' : [], 'left' : [], 'right' : [],
            'right_idle' : [], 'left_idle' : [], 'up_idle' : [], 'down_idle' : [],
            'right_attack' : [], 'left_attack' : [], 'up_attack' : [], 'down_attack' : [],
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status: # If we are attacking we do not want the player to play the idle animation
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if not 'attack' in self.status: # if not attacking
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else :
                    self.status = self.status + '_attack'
        else :
            if ('attack' in self.status):
                self.status = self.status.replace('_attack', '')

    def input(self): # key input
        if not self.attacking:
            keys = pygame.key.get_pressed() # get all keys pressed

            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.status = 'down'
                self.direction.y = 1
            else :
                self.direction.y = 0


            if keys[pygame.K_LEFT]:
                self.status = 'left'
                self.direction.x = -1
            elif keys[pygame.K_RIGHT]:
                self.status = 'right'
                self.direction.x = 1
            else :
                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # magic imput
            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                self.weapon = list(weapon_data.keys())[self.weapon_index % len(list(weapon_data.keys()))]

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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)