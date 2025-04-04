import os
import pygame
from objects import Meow, PointCollector, CloudSpawner
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

if __name__=="__main__":
    InitializeGame()
