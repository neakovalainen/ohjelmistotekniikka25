import os
import pygame_textinput
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
        self.textinput = pygame_textinput.TextInputVisualizer()
        self.game_started = False
        self.game_over = False

        self.add_sprites()
        self.text_input()
        self.game_loop()

    def display(self):
        self.screen.fill("white")
        text, start, user_guide1, user_guide2 = self.text_objects()

        #pygame.draw.rect(self.screen, "black", self.player.rect) # rect for debugging
        #pygame.draw.rect(self.screen, "red", self.cloudspawner.rect)
        self.screen.blit(self.player.meow, (self.player.x, self.player.y))
        self.screen.blit(self.energy.img, (self.energy.x, self.energy.y))
        self.screen.blit(self.cloudspawner.img1, (self.cloudspawner.x, self.cloudspawner.y))
        self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        self.screen.blit(text, (20, 20))
        self.screen.blit(start, (300, 20))
        self.screen.blit(self.textinput.surface, (10, 140))
        self.screen.blit(user_guide1, (10, 100))
        self.screen.blit(user_guide2, (10, 120))
        pygame.display.set_caption("cloudleap")
        pygame.display.flip()

    def game_loop(self):
        while True:
            if not self.game_started:
                self.space_check()
            self.event_check()
            self.position_check(self.energy, self.enemy, self.cloudspawner, self.game_started)
            self.moving_check(self.player)
            self.collision_check(self.player, self.energy, self.enemy, self.game_over)
            self.energy.update_rects(self.player, self.cloudspawner, self.enemy)
            self.display()
            self.clock.tick(60)

    def event_check(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        self.textinput.update(events)

    def moving_check(self, player):
        player.forward_check()
        player.backwards_check()
        player.jump_check()

    def position_check(self, energy, enemy, cloudspawner, game_started):
        energy.obtainableposition(game_started)
        cloudspawner.cloudposition(game_started)
        enemy.enemy_position(game_started)

    def collision_check(self, player, energy, enemy, game_over):
        self.energy.collision_detector(player, energy)
        self.cloudspawner.cloudcollision(player)
        self.enemy.negative_collision(player, energy, enemy, game_over)

    def space_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.game_started = True

    def text_input(self):
        self.textinput.cursor_width = 1
        self.textinput.cursor_blink_interval = 500
        self.textinput.font_object = pygame.font.Font("src/assets/unifont-16.0.02.otf", 15)

    def text_objects(self):
        lil_font = pygame.font.Font("src/assets/unifont-16.0.02.otf", 15)
        self.text = self.font.render("current energy:" + str(self.energy.points), True, ("black"))
        self.start = self.font.render("start game by pressing space (づ ◕‿◕ )づ", True, ("black"))
        self.guide1 = lil_font.render("write username below, if it doesn't exist,", True, ("black"))
        self.guide2 = lil_font.render("it will be created automatically:", True, ("black"))
        return self.text, self.start, self.guide1, self.guide2

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
