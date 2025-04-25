import os
import pygame
from objects import Meow, PointCollector, CloudSpawner, MinusEnergy
from userdata import UserData
from textmanager import TextManager
from shared_resources import status, game_status
from sql_connect import get_database_connection
from game_over import GameOver

# game character created by @snackanimals on twitter/X
dirname = os.path.dirname(__file__)

GROUND_HEIGHT = 500

class InitializeGame():
    def __init__(self):
        pygame.init()
        self.player = Meow(550, GROUND_HEIGHT)
        self.energy = PointCollector()
        self.cloudspawner = CloudSpawner(1500, 500)
        self.enemy = MinusEnergy(3000, 600)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.user_data = UserData(get_database_connection())
        self.textmanager = TextManager(self.energy, self.screen, self.user_data)

        self.game_loop()

    def display(self):
        self.screen.fill("white")
        #pygame.draw.rect(self.screen, "black", self.player.rect) # rect for debugging
        #pygame.draw.rect(self.screen, "red", self.cloudspawner.rect)
        self.screen.blit(self.player.meow, (self.player.x, self.player.y))
        for energy in self.energy.all_energies:
            #print(energy[0], energy[1])
            self.screen.blit(self.energy.img, (energy[0], energy[1]))
        self.screen.blit(self.cloudspawner.img1, (self.cloudspawner.x, self.cloudspawner.y))
        self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        if not status.logged_in:
            self.screen.blit(self.textmanager.textinput.surface, (10, 160))
        self.textmanager.draw_texts()
        pygame.draw.line(self.screen, ("black"), (0, 640), (1280, 640))
        pygame.display.set_caption("cloudleap")

    def game_loop(self):
        while True:
            if status.logged_in:
                if not game_status.game_started:
                    self.space_check()
            if not game_status.game_over:
                self.position_check(self.energy, self.enemy, self.cloudspawner)
                self.moving_check(self.player)
                self.energy.update_rects(self.player, self.cloudspawner, self.enemy)
                self.collision_check(self.player, self.energy, self.enemy)
                self.display()
                self.event_check()
            else:
                GameOver(self.screen).game_over_display(7000)
                self.energy.best_score = self.energy.points
                if self.user_data.get_score(status.username) < self.energy.best_score:
                    self.user_data.update_score(self.energy.best_score, status.username)
                pygame.quit()
                break
            pygame.display.flip()
            self.clock.tick(60)

    def event_check(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                status.login()
                username = self.textmanager.textinput.value
                status.current_user(username)
                if not self.username_check(username):
                    self.user_data.save_username(username)
                self.user_data.get_all_scores()

        if not status.logged_in:
            self.textmanager.textinput.update(events)
        self.textmanager.button_update(events)

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

    def position_check(self, energy, enemy, cloudspawner):
        energy.obtainableposition()
        cloudspawner.cloudposition()
        enemy.enemy_position()

    def collision_check(self, player, energy, enemy):
        self.energy.collision_detector(player, energy)
        self.cloudspawner.cloudcollision(player)
        self.enemy.negative_collision(player, energy, enemy)

    def space_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_status.change_game_status()

if __name__=="__main__":
    InitializeGame()
