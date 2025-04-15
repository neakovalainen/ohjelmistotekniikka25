import unittest
from index import InitializeGame, GROUND_HEIGHT
from objects import Meow, PointCollector, CloudSpawner, MinusEnergy
from shared_resources import game_status, LogInManager, GameStatus

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.player = Meow(500, GROUND_HEIGHT)
        self.game = InitializeGame
        game_status.game_started = True

    def test_player_x_coordinate_initialized_correctly(self):
        self.assertEqual((self.player.x, self.player.y), (500, GROUND_HEIGHT))

    def test_points_increased_when_collision_happens(self):
        self.energy = PointCollector(500, GROUND_HEIGHT)
        self.energy.collision_detector(self.player, self.energy)
        self.assertEqual(self.energy.points, 1)

    def test_cloud_spawns_outside_screen_if_dissappeared_from_left(self):
        self.cloud = CloudSpawner(-600, 500)
        self.cloud.cloudposition()
        self.assertTrue(1280 <= self.cloud.x <= 2000)
    
    def test_cloud_moves_left_while_on_screen(self):
        self.cloud = CloudSpawner(100, 500)
        self.cloud.cloudposition()
        self.assertEqual(self.cloud.x, 96)

    def test_energy_drink_spawns_outside_screen_if_disappeared_from_left(self):
        self.energy = PointCollector(-3, 500)
        self.energy.obtainableposition()
        self.assertTrue(1280 <= self.energy.x <= 2000)

    def test_energy_drink_moves_left_while_on_screen(self):
        self.energy = PointCollector(500, GROUND_HEIGHT)
        self.energy.obtainableposition()
        self.assertEqual(self.energy.x, 496)

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
        enemy = MinusEnergy(500, GROUND_HEIGHT)
        self.assertEqual((enemy.x, enemy.y), (500, GROUND_HEIGHT))