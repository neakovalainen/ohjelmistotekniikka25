import os
import pygame
from objects import Meow, PointCollector, CloudSpawner, MinusEnergy
from database.userdata import UserData
from textmanager import TextManager
from shared_resources import status, game_status
from database.sql_connect import get_database_connection
from game_over import GameOver

# game character created by @snackanimals on twitter/X
dirname = os.path.dirname(__file__)

GROUND_HEIGHT = 500

class InitializeGame():
    """ 
        Luokka, jonka avulla peli käynnistetään ja suljetaan ja, joka pitää huolta 
        sen pyörittämisestä
    """
    def __init__(self):
        pygame.init()
        self.player = Meow()
        self.energy = PointCollector()
        self.cloud = CloudSpawner()
        self.enemy = MinusEnergy()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.data = UserData(get_database_connection())
        self.textmanager = TextManager(
            self.player, self.energy, self.cloud, self.enemy, self.screen, self.data)
        self.running = True
        self.game_loop()

    def display(self):
        """
            huolehtii objektien ja taustan piirtämisestä näytölle
        """
        self.screen.fill("white")
        self.screen.blit(self.player.meow, (self.player.x, self.player.y))
        for energy in self.energy.all_energies:
            self.screen.blit(self.energy.img, (energy[0], energy[1]))
        for cloud in self.cloud.clouds:
            self.screen.blit(self.cloud.img1, (cloud[0], cloud[1]))
        self.screen.blit(self.enemy.img, (self.enemy.x, self.enemy.y))
        if not status.logged_in:
            self.screen.blit(self.textmanager.textinput.surface, (10, 160))
        self.textmanager.draw_texts()
        if status.display_error == True:
            self.textmanager.error_message()
        pygame.draw.line(self.screen, ("black"), (0, 640), (1280, 640))
        pygame.display.set_caption("cloudleap")

    def game_loop(self):
        """
            hoitaa pelin pyörittämisen niin kauan kun self.running = True
        """
        while self.running:
            if status.logged_in:
                if not game_status.game_started:
                    self.space_check()
            if not game_status.game_over:
                if game_status.game_started:
                    self.position_check(self.energy, self.enemy, self.cloud)
                    self.moving_check(self.player)
                    self.energy.update_rects(self.player, self.cloud, self.enemy)
                    self.collision_check(self.player, self.energy, self.enemy)
                self.display()
                self.event_check()
                if not self.running:
                    break
            else:
                GameOver(self.screen, self.energy.points).game_over_display(8000)
                self.energy.best_score = self.energy.points
                self.textmanager.update_scores()
                break
            pygame.display.flip()
            self.clock.tick(60)

    def event_check(self):
        """
            Tarkistaa tapahtumat, joiden perusteella uusi käyttäjä tallennetaan,
            tulokset haetaan tietokannasta ja peli-ikkuna suljetaan
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if " " in self.textmanager.textinput.value or len(self.textmanager.textinput.value) < 1:
                    status.display_error = True
                else:
                    status.display_error = False
                    status.login()
                    username = self.textmanager.textinput.value
                    status.current_user(username)
                    if not self.data.get_username(username):
                        self.data.save_username(username)

        if not status.logged_in:
            self.textmanager.textinput.update(events)
        self.textmanager.button_update(events)

    def moving_check(self, player):
        """
            Pelaajan liikkumisen tarkistus, lisätty erilliseen metodiin, jotta
            koodi olisi helpommin luettavaa

            Args:
            player: pelaaja
        """
        player.forward_check()
        player.backwards_check()
        player.jump_check()

    def position_check(self, energy, enemy, cloud):
        energy.obtainableposition(cloud)
        cloud.cloudposition()
        enemy.enemy_position()

    def collision_check(self, player, energy, enemy):
        self.energy.collision_detector(player, energy)
        self.cloud.cloudcollision(player)
        self.enemy.negative_collision(player, energy, enemy)

    def space_check(self):
        """
            Peli aloitetaan painamalla space, tämä tarkistaa sen
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_status.change_game_status()

if __name__=="__main__":
    InitializeGame()
