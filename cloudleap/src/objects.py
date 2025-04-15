import os
import random
import pygame
from shared_resources import game_status
# game character created by @snackanimals on twitter/X
dirname = os.path.dirname(__file__)

GROUND_HEIGHT = 500

class Meow(pygame.sprite.Sprite): # player location, movement etc.
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('src/assets/meowmeow.png')
        self.meow = pygame.transform.scale(self.image, (105, 142)) # right size image
        self.x = x
        self.y = y
        self.jumping = False
        self.jump_force = 20
        self.rect = pygame.Rect(self.x, self.y, self.meow.get_width(), self.meow.get_height())

    def jump_check(self):
        if not self.jumping:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.jumping = True

        if self.jumping:
            self.y -= self.jump_force
            self.jump_force -= 0.60

            if GROUND_HEIGHT <= self.y:
                self.y = GROUND_HEIGHT
                self.jumping = False
                self.jump_force = 20

    def is_falling(self):
        return self.jump_force < 0

    def forward_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x <= 1280 - self.meow.get_width():
            self.x += 2

    def backwards_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 2


class PointCollector(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('src/assets/energy.png')
        self.img = pygame.transform.scale(self.image, (13, 38))
        self.x = x
        self.y = y
        self.points = 0
        self.best_score = 0
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def obtainableposition(self):
        if game_status.game_started:
            if self.x < 0:
                self.x = random.randint(1280, 2000)
            else:
                self.x -= 4

    def energy_consumed(self):
        self.x += random.randint(1280, 2000)

    def collision_detector(self, player, energy):
        if pygame.sprite.collide_rect(player, energy):
            self.points += 1
            self.energy_consumed()

    def update_rects(self, meow, cloud, enemy):
        self.rect.topleft = (self.x, self.y)
        meow.rect.topleft = (meow.x, meow.y)
        cloud.rect.topleft = (cloud.x, cloud.y)
        enemy.rect.topleft = (enemy.x, enemy.y)


class CloudSpawner(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img1 = pygame.image.load('src/assets/pilvi1.png')
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.img1.get_width(), self.img1.get_height())

    def cloudposition(self):
        if game_status.game_started:
            if self.x < -500:
                self.x = random.randint(1280, 2000)
            else:
                self.x -= 4

    def cloudcollision(self, player):
        player_next_pos = player.rect.bottom + player.jump_force

        left_in_cloud = self.rect.left < player.rect.left and player.rect.left < self.rect.right
        right_in_cloud = self.rect.left < player.rect.right and player.rect.right < self.rect.right

        in_cloud = left_in_cloud or right_in_cloud
        would_touch = self.rect.top < player_next_pos and player_next_pos < self.rect.bottom

        above_ground = player.y < GROUND_HEIGHT

        distance = abs((player.rect.left + player.meow.get_width()) - self.rect.right)

        if player.is_falling() and in_cloud and would_touch:
            player.jumping = False

        if not in_cloud and above_ground and player.rect.left > self.rect.right and distance < 200:
            player.y += 10

class MinusEnergy:
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('src/assets/computarr.png')
        self.img = pygame.transform.scale(self.image, (64, 61.5))
        self.x = x
        self.y = y
        self.enemies_hit = 0
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def negative_collision(self, player, energy, enemy):
        if pygame.sprite.collide_rect(player, enemy):
            energy.points -= 1
            self.enemies_hit += 1
            self.enemy_hit(energy)

    def enemy_position(self):
        if game_status.game_started:
            if self.x < 0:
                self.x = random.randint(1280, 1500)
            else:
                self.x -= 4

    def enemy_hit(self, energy):
        if energy.points < 0:
            game_status.game_lost()
        if self.enemies_hit >= 3:
            game_status.game_lost()
        else:
            self.x = random.randint(1280, 2000)
