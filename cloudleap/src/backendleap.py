import pygame
import os
# game character created by @snackanimals on twitter/X
dirname = os.path.dirname(__file__)

class InitializeGame(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        super().__init__()

        self.player = Meow(550, 500) # create a player
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.energy = PointCollector() # create and position collectables
        self.obstaclespawner = ObstacleSpawner()
        self.sprites = pygame.sprite.Group() # creates a group of all sprites, to keep track of collision
        self.add_sprites()
        self.game_loop()

    def close_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def display(self):
        self.screen.fill("white")
        self.screen.blit(self.player.meow, (self.player.x, self.player.y))
        self.screen.blit(self.energy.img, (self.energy.x, self.energy.y))
        pygame.display.set_caption("cloudleap")
        pygame.display.flip()

    def game_loop(self):
        running = True

        while running:
            self.close_check()
            self.player.forward_check()
            self.player.backwards_check() 
            self.player.jump_check()
            self.display()
            self.clock.tick(60)

    def add_sprites(self):
        self.sprites.add(self.player)

class Meow(pygame.sprite.Sprite): # player location, movement etc.
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('src/assets/meowmeow.png')
        self.meow = pygame.transform.scale(self.image, (105, 142)) # right size image
        self.x = x
        self.y = y
        self.jumping = False
        self.jump_force = 20
        # self.rect = self.meow.get_rect()

    def jump_check(self):
        if self.jumping == False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.jumping = True
        
        if self.jumping:
            self.y -= self.jump_force
            self.jump_force -= 1

            if self.jump_force < -20:
                self.jumping = False
                self.jump_force = 20

    def forward_check(self):    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x <= 1280 - self.meow.get_width():
            self.x += 2

    def backwards_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 2

        

class PointCollector: # collectable
    def __init__(self):
        self.image = pygame.image.load('src/assets/energy.png')
        self.img = pygame.transform.scale(self.image, (34, 95)) #right size image
        self.x = 700
        self.y = 500
        self.points = 0
        self.best_score = 0
    
    def obtainableposition():
        # function for collectable item spawning
        pass

class ObstacleSpawner:
    def __init__(self):
        pass

if __name__=="__main__":
    InitializeGame()