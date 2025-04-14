import os
import pygame
from objects import Meow, PointCollector, CloudSpawner, MinusEnergy
from userdata import UserData
from textmanager import TextManager
from sql_connect import get_database_connection
# game character created by @snackanimals on twitter/X
dirname = os.path.dirname(__file__)

GROUND_HEIGHT = 500

class InitializeGame():
    def __init__(self):
        pygame.init()

        self.player = Meow(550, GROUND_HEIGHT)
        self.energy = PointCollector(1700, 600)
        self.cloudspawner = CloudSpawner(1500, 500)
        self.enemy = MinusEnergy(3000, 600)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("src/assets/unifont-16.0.02.otf", 30)
        self.sprites = pygame.sprite.Group() # group of all sprites, keeps track of collision
        self.user_data = UserData(get_database_connection())
        self.textmanager = TextManager(self.energy, self.screen, self.user_data)
        self.game_started = False
        self.game_over = False
        self.logging_in = True

        self.add_sprites()
        self.game_loop()

    def display(self):
        self.screen.fill("white")
        #pygame.draw.rect(self.screen, "black", self.player.rect) # rect for debugging
        #pygame.draw.rect(self.screen, "red", self.cloudspawner.rect)
        self.screen.blit(self.player.meow, (self.player.x, self.player.y))
        self.screen.blit(self.energy.img, (self.energy.x, self.energy.y))
        self.screen.blit(self.cloudspawner.img1, (self.cloudspawner.x, self.cloudspawner.y))
        self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        if self.logging_in:
            self.screen.blit(self.textmanager.textinput.surface, (10, 140))
        self.textmanager.draw_texts()
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.logging_in = False
                username = self.textmanager.textinput.value
                self.textmanager.username_update(username)
                if not self.username_check(username):
                    self.user_data.save_username(username)
                self.user_data.get_all_users()

        if self.logging_in:
            self.textmanager.textinput.update(events)

    def username_check(self, username):
        all_users = self.user_data.get_all_users()
        for _, user in all_users:
            if username == user:
                return True
        return False


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
