import unittest

import pygame.tests
from index import GROUND_HEIGHT
from objects import Meow, PointCollector, CloudSpawner, MinusEnergy
from shared_resources import game_status, LogInManager, GameStatus
import pygame

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.player = Meow()
        self.energy = PointCollector()
        self.cloud = CloudSpawner()
        self.enemy = MinusEnergy()
        game_status.game_started = True

    def test_player_x_coordinate_initialized_correctly(self):
        self.assertEqual((self.player.x, self.player.y), (500, GROUND_HEIGHT))

    def test_points_increased_when_collision_happens(self):
        self.energy.all_energies = [(500, GROUND_HEIGHT)]
        self.energy.add_rects()
        self.energy.collision_detector(self.player, self.energy)
        self.assertEqual(self.energy.points, 1)

    def test_cloud_spawns_outside_screen_if_dissappeared_from_left(self):
        self.cloud.clouds = [(-600, 500)]
        self.cloud.cloudposition()
        self.assertTrue(1280 <= self.cloud.clouds[0][0] <= 4000)
    
    def test_cloud_moves_left_while_on_screen(self):
        self.cloud.clouds = [(100, 500)]
        self.cloud.cloudposition()
        self.assertEqual(self.cloud.clouds[0][0], 96)

    def test_energy_drink_spawns_outside_screen_if_disappeared_from_left(self):
        self.energy.all_energies = [(-100, 600)]
        self.energy.obtainableposition(self.cloud)
        self.assertTrue(1280 <= self.energy.all_energies[0][0] <= 5000)

    def test_energy_drink_moves_left_while_on_screen(self):
        self.energy.all_energies = [(500, 500)]
        self.energy.obtainableposition(self.cloud)
        self.assertEqual(self.energy.all_energies[0][0], 496)

    def test_player_jumps_y_decreases(self):
        jump_force = self.player.jump_force
        self.player.jumping = True
        self.player.jump_check()
        self.assertEqual(self.player.y, GROUND_HEIGHT - jump_force)

    def test_player_jumps_and_GROUND_HEIGHT_lower_than_player_y_equal_to_GROUND_HEIGHT(self):
        self.player.y = 700
        self.player.jumping = True
        self.player.jump_check()
        self.assertEqual(self.player.y, GROUND_HEIGHT)

    def test_is_falling_returns_True(self):
        self.player.jump_force = -1
        self.assertEqual(self.player.is_falling(), True)
    
    def test_is_falling_returns_False(self):
        self.player.jump_force = 1
        self.assertEqual(self.player.is_falling(), False)


    def test_loginmanager_login_works(self):
        loginmanager = LogInManager()
        loginmanager.login()
        self.assertEqual(loginmanager.logged_in, True)

    def test_loginmanager_logout_works(self):
        loginmanager = LogInManager()
        loginmanager.logged_in = True
        loginmanager.logout()
        self.assertEqual(loginmanager.logged_in, False)
    
    def test_current_username_function_works(self):
        loginmanager = LogInManager()
        loginmanager.current_user("test_user")
        self.assertEqual(loginmanager.username, "test_user")

    def test_change_game_status_works_if_game_started_False(self):
        status = GameStatus()
        status.change_game_status()
        self.assertEqual(status.game_started, True)

    def test_change_game_status_works_if_game_started_True(self):
        status = GameStatus()
        status.game_started = True
        status.change_game_status()
        self.assertEqual(status.game_started, False)

    def test_game_over_works(self):
        status = GameStatus()
        status.game_lost()
        self.assertEqual(status.game_over, True)

    def test_enemy_position_initialized_correctly(self):
        enemy = MinusEnergy()
        self.assertEqual((enemy.x, enemy.y), (3000, 600))

    def test_start_falling_jumping_True(self):
        self.player.start_falling()
        self.assertEqual(self.player.jumping, True)
    
    def test_start_falling_jump_force_to_zero(self):
        self.player.start_falling()
        self.assertEqual(self.player.jump_force, 0)

    def test_touching_cloud_into_False_if_jumping(self):
        self.player.touching_cloud = True
        self.player.jumping = True
        self.player.jump_check()
        self.assertEqual(self.player.touching_cloud, False)

    def test_energy_reset(self):
        self.energy.points = 10
        self.energy.reset_stats()
        self.assertEqual(self.energy.points, 0)

    def test_reset_energy_positions(self):
        self.energy.all_energies = ((1,2), (3, 4))
        self.energy.start_positions()
        self.assertEqual(len(self.energy.all_energies), 5)

    def test_reset_cloud_positions(self):
        self.cloud.clouds = ((1,2), (2, 3))
        self.cloud.start_positions()
        self.assertEqual(len(self.cloud.clouds), 3)
    
    def test_enemy_new_position_if_disappeared_from_left(self):
        self.enemy.x = -100
        self.enemy.y = 500
        self.enemy.enemy_position()
        self.assertTrue(1280 <= self.enemy.x <= 3000)