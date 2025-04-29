import os
import random
import pygame
from shared_resources import game_status
# game character created by @snackanimals on twitter/X
dirname = os.path.dirname(__file__)

GROUND_HEIGHT = 500

class Meow(pygame.sprite.Sprite):
    """
        Luokka, joka sisältää käytännössä kaiken tiedon pelaajasta ja
        hoitaa sen liikkumista
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('src/assets/meowmeow.png')
        self.meow = pygame.transform.scale(self.image, (105, 142))
        self.x = 0
        self.y = 0
        self.touching_cloud = False
        self.jumping = False
        self.jump_force = 20
        self.rect = pygame.Rect(self.x, self.y, self.meow.get_width(), self.meow.get_height())

        self.start_position()

    def start_position(self):
        """
            Pelaajan sijainti pelin alkaessa
        """
        self.x = 500
        self.y = GROUND_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.meow.get_width(), self.meow.get_height())

    def reset_jumping(self):
        self.jumping = False
        self.jump_force = 20

    def jump_check(self):
        """
            Metodi hyppäämisen toteuttamiselle
            seuraa hyppääkö pelaaja ja jos on hypännyt pitää huolen
            sen laskeutumisesta
        """
        if not self.jumping:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.jumping = True

        if self.jumping:
            self.y -= self.jump_force
            self.jump_force -= 0.60

            if GROUND_HEIGHT <= self.y:
                self.y = GROUND_HEIGHT
                self.reset_jumping()

            if self.touching_cloud:
                self.touching_cloud = False

    def is_falling(self):
        """
            Tarkistus onko pelaaja putoamassa
        """
        return self.jump_force < 0

    def start_falling(self):
        self.jumping = True
        self.jump_force = 0

    def forward_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x <= 1280 - self.meow.get_width():
            self.x += 2

    def backwards_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 2


class PointCollector(pygame.sprite.Sprite):
    """
        Luokka, joka sisältää tiedot liittyen pisteiden keruuseen ja 
        energiajuomien liikkumiseen
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('src/assets/energy.png')
        self.img = pygame.transform.scale(self.image, (13, 38))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.points = 0
        self.best_score = 0
        self.all_energies = []
        self.energy_rects = []
        self.start_positions()
        self.add_rects()

    def reset_stats(self):
        self.points = 0
        game_status.energy_level = 4

    def start_positions(self):
        """
            Kun peli alkaa tai käyttäjä kirjautuu ulos
            sijainnit määritellään uudestaan
        """
        if len(self.all_energies) > 0:
            self.all_energies = []
        for _ in range(5):
            x = random.randint(1280, 5000)
            y = 600
            self.all_energies.append((x, y))

    def add_rects(self):
        """
            Rectit juomien kohdalle, jotta voidaan seurata collisiota
        """
        if len(self.energy_rects) > 0:
            self.energy_rects = []
        for energy in self.all_energies:
            self.energy_rects.append(pygame.Rect(energy[0], energy[1], self.width, self.height))

    def spawn_on_cloud(self, cloud):
        """
            Aina välillä juoma pilven päälle
        """
        if random.choice([True, False]):
            for cloud_location in cloud.clouds:
                if cloud_location[0] > 1280:
                    return (cloud_location[0] + 50, cloud_location[1] - 20)
        return (random.randint(1280, 5000), 600)

    def obtainableposition(self, cloud):
        """
            Pitää huolen energiajuomien liikkumisesta

            Args:
                cloud: lista pilvistä, josta etsitään joku
                minkä päälle energiajuoman voi laittaa
        """
        if game_status.game_started:
            for index, energy in enumerate(self.all_energies):
                x = energy[0]
                if x < 0:
                    self.all_energies[index] = self.spawn_on_cloud(cloud)
                else:
                    x -= game_status.energy_level
                    self.all_energies[index] = (x, energy[1])

    def energy_consumed(self, energy):
        """
            Kollision jälkeen energiajuoma spawnaa ruudun ulkopuolelle

            Args:
                energy: energiajuoma
        """
        x = energy[0]
        x += random.randint(1280, 2000)
        return x, 600

    def collision_detector(self, player, energy):
        """
            Seuraa tapahtuuko pelaajan ja energiajuoman välillä
            kollisiota
        """
        for rect in energy.energy_rects:
            if rect.colliderect(player.rect):
                possible_collision = [
                    (x, y) for (x, y) in energy.all_energies if rect.x <= x <= rect.x + rect.width]
                if len(possible_collision):
                    index = energy.all_energies.index(possible_collision[0])
                    energy.all_energies[index] = self.energy_consumed(energy.all_energies[index])
                    self.points += 1
                    game_status.energy_level += 0.25

    def update_rects(self, meow, cloud, enemy):
        for index, energy in enumerate(self.all_energies):
            self.energy_rects[index] = pygame.Rect(energy[0], energy[1], self.width, self.height)
        for index, current_cloud in enumerate(cloud.clouds):
            cloud.cloud_rects[index] = pygame.Rect(
                current_cloud[0], current_cloud[1], cloud.width, cloud.height)
        meow.rect.topleft = (meow.x, meow.y)
        enemy.rect.topleft = (enemy.x, enemy.y)


class CloudSpawner(pygame.sprite.Sprite):
    """
        Luokka, joka hoitaa pilvien liikuttamisen ja 
        mahdollistaa niiden päälle hyppäämisen
    """

    def __init__(self):
        super().__init__()
        self.img1 = pygame.image.load('src/assets/pilvi1.png')
        self.width = self.img1.get_width()
        self.height = self.img1.get_height()
        self.clouds = []
        self.cloud_rects = []
        self.start_positions()
        self.add_rects()

    def start_positions(self):
        """
            Pilvien sijainnit pelin alussa, päivitetään uloskirjautumisen
            ja pelin käynnistämisen yhteydessä
        """
        if len(self.clouds) > 0:
            self.clouds = []
        for _ in range(3):
            x = random.randint(1280, 4000)
            y = random.randint(350, 520)
            self.clouds.append((x, y))

    def add_rects(self):
        if len(self.cloud_rects) > 0:
            self.cloud_rects = []
        for cloud in self.clouds:
            self.cloud_rects.append(pygame.Rect(cloud[0], cloud[1], self.width, self.height))

    def cloudposition(self):
        if game_status.game_started:
            for index, cloud in enumerate(self.clouds):
                x, y = cloud[0], cloud[1]
                if x < -500:
                    x = random.randint(1280, 4000)
                    y = random.randint(350, 520)
                    self.clouds[index] = (x, y)
                else:
                    x -= game_status.energy_level
                    self.clouds[index] = (x, y)

    def cloudcollision(self, player):
        """
            Metodi, joka mahdollistaa pilvien päälle hyppäämisen
            ja niiden päältä putoamisen

            Args:
                player: pelaaja
        """
        was_touching_cloud = player.touching_cloud
        player.touching_cloud = False

        player_next_pos = player.rect.bottom + player.jump_force
        for rect in self.cloud_rects:
            left, right = rect.x, rect.x + self.width
            top, bottom = rect.y, rect.y + self.height

            left_in_cloud = left < player.rect.left and player.rect.left < right
            right_in_cloud = left < player.rect.right and player.rect.right < right

            in_cloud = left_in_cloud or right_in_cloud
            would_touch = top < player_next_pos and player_next_pos < bottom

            if player.is_falling() and in_cloud and would_touch:
                player.touching_cloud = True
                player.reset_jumping()

        if was_touching_cloud and not player.touching_cloud:
            player.start_falling()

class MinusEnergy:
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('src/assets/computarr.png')
        self.img = pygame.transform.scale(self.image, (64, 61.5))
        self.x = 0
        self.y = 0
        self.enemies_hit = 0
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

        self.start_position()

    def start_position(self):
        self.x = 3000
        self.y = 600
        self.enemies_hit = 0

    def negative_collision(self, player, energy, enemy):
        if pygame.sprite.collide_rect(player, enemy):
            energy.points -= 1
            self.enemies_hit += 1
            self.enemy_hit(energy)
            game_status.energy_level -= 0.5

    def enemy_position(self):
        if game_status.game_started:
            if self.x < 0:
                self.x = random.randint(1280, 3000)
            else:
                self.x -= game_status.energy_level

    def enemy_hit(self, energy):
        if energy.points < 0:
            energy.points = 0
            game_status.game_lost()
        if self.enemies_hit >= 3:
            game_status.game_lost()
        else:
            self.x = random.randint(1280, 5000)
