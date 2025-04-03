import os
import pygame
import random
# game character created by @snackanimals on twitter/X
dirname = os.path.dirname(__file__)

GROUND_HEIGHT = 500

class InitializeGame():
    def __init__(self):
        pygame.init()

        self.player = Meow(550, GROUND_HEIGHT) # create a player
        self.screen = pygame.display.set_mode((1280, 720))
        self.font = pygame.font.SysFont("Times New Roman", 30)
        self.clock = pygame.time.Clock()
        self.energy = PointCollector(1000, 600) # create and position collectables
        self.cloudspawner = CloudSpawner(700, 500)
        self.sprites = pygame.sprite.Group() # group of all sprites, keeps track of collision
        self.add_sprites()
        self.game_loop()

    def close_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def display(self):
        self.screen.fill("white")
        #pygame.draw.rect(self.screen, "black", self.player.rect) # rect for debugging
        #pygame.draw.rect(self.screen, "red", self.cloudspawner.rect)
        self.screen.blit(self.player.meow, (self.player.x, self.player.y))
        self.screen.blit(self.energy.img, (self.energy.x, self.energy.y))
        self.screen.blit(self.cloudspawner.img1, (self.cloudspawner.x, self.cloudspawner.y))
        text = self.font.render("current energy:" + str(self.energy.points), True, ("black"))
        self.screen.blit(text, (20, 20))
        pygame.display.set_caption("cloudleap")
        pygame.display.flip()

    def game_loop(self):
        running = True

        while running:
            self.close_check()
            self.energy.obtainableposition()
            self.cloudspawner.cloudposition()
            self.player.forward_check()
            self.player.backwards_check()
            self.player.jump_check()
            self.energy.collision_detector(self.player, self.energy)
            self.cloudspawner.cloudcollision(self.player)
            self.energy.update_rects(self.player, self.cloudspawner)
            self.display()
            self.clock.tick(60)

    def add_sprites(self):
        #self.sprites.add(self.player)
        #self.sprites.add(self.energy)
        #self.sprites.add(self.energy)
        # print("Player rect:", self.player.rect)
        # print("Obtainable rect:", self.energy.rect)
        # print("cloud rect:", self.cloudspawner.rect)
        pass

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

        self.left, self.right = self.x, self.x + self.meow.get_width()

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


class PointCollector(pygame.sprite.Sprite): # collectable
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('src/assets/energy.png')
        self.img = pygame.transform.scale(self.image, (13, 38)) #right size image
        self.x = x
        self.y = y
        self.points = 0
        self.best_score = 0
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def obtainableposition(self):
        # function for collectable item spawning/movement
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

    def update_rects(self, meow, cloud):
        self.rect.topleft = (self.x, self.y)
        meow.rect.topleft = (meow.x, meow.y)
        cloud.rect.topleft = (cloud.x, cloud.y)


class CloudSpawner(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img1 = pygame.image.load('src/assets/pilvi1.png')
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.img1.get_width(), self.img1.get_height())
    
    def cloudposition(self):
        if self.x < -500:
            self.x = random.randint(1280, 2000)
        else:
            self.x -= 4

    def cloudcollision(self, player):
        player_next_location = player.rect.bottom + player.jump_force 

        left_in_cloud = self.rect.left < player.rect.left and player.rect.left < self.rect.right
        right_in_cloud = self.rect.left < player.rect.right and player.rect.right < self.rect.right

        in_cloud = left_in_cloud or right_in_cloud
        would_touch = self.rect.top < player_next_location and player_next_location < self.rect.bottom

        above_ground = player.y < GROUND_HEIGHT

        distance = abs((player.rect.left + player.meow.get_width()) - self.rect.right)

        if player.is_falling() and in_cloud and would_touch:
            player.jumping = False

        if not in_cloud and above_ground and player.rect.left > self.rect.right and distance < 200:
            player.y += 10


        


if __name__=="__main__":
    InitializeGame()
