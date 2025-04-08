import os
import pygame
from objects import Meow, PointCollector, CloudSpawner, MinusEnergy
# game character created by @snackanimals on twitter/X
dirname = os.path.dirname(__file__)

GROUND_HEIGHT = 500

class InitializeGame():
    def __init__(self):
        pygame.init()

        self.player = Meow(550, GROUND_HEIGHT) # create a player
        self.energy = PointCollector(1700, 600) # create and position collectables
        self.cloudspawner = CloudSpawner(1500, 500)
        self.enemy = MinusEnergy(3000, 600)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("src/assets/unifont-16.0.02.otf", 30)
        self.sprites = pygame.sprite.Group() # group of all sprites, keeps track of collision
        self.add_sprites()
        self.game_started = False
        self.game_loop()

    def close_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def display(self):
        self.screen.fill("white")
        self.font = pygame.font.Font("src/assets/unifont-16.0.02.otf", 30)
        #pygame.draw.rect(self.screen, "black", self.player.rect) # rect for debugging
        #pygame.draw.rect(self.screen, "red", self.cloudspawner.rect)
        self.screen.blit(self.player.meow, (self.player.x, self.player.y))
        self.screen.blit(self.energy.img, (self.energy.x, self.energy.y))
        self.screen.blit(self.cloudspawner.img1, (self.cloudspawner.x, self.cloudspawner.y))
        self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        text = self.font.render("current energy:" + str(self.energy.points), True, ("black"))
        start = self.font.render("start game by pressing space (づ ◕‿◕ )づ", True, ("black"))
        self.screen.blit(text, (20, 20))
        self.screen.blit(start, (300, 20))
        pygame.display.set_caption("cloudleap")
        pygame.display.flip()


    def game_loop(self):
        running = True

        while running:
            if not self.game_started:
                self.space_check()
            self.close_check()
            self.energy.obtainableposition(self.game_started)
            self.cloudspawner.cloudposition(self.game_started)
            self.enemy.enemy_position(self.game_started)
            self.moving_check()
            self.energy.collision_detector(self.player, self.energy)
            self.cloudspawner.cloudcollision(self.player)
            self.enemy.negative_collision(self.player, self.energy, self.enemy)
            self.energy.update_rects(self.player, self.cloudspawner, self.enemy)
            self.display()
            self.clock.tick(60)

    def moving_check(self):
        self.player.forward_check()
        self.player.backwards_check()
        self.player.jump_check()

    def space_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.game_started = True



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
