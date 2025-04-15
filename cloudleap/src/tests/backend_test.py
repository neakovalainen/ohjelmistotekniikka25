import unittest
from index import InitializeGame
from objects import Meow, PointCollector, CloudSpawner
from shared_resources import game_status

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.player = Meow(500, 550)
        self.game = InitializeGame
        game_status.game_started = True

    def test_player_x_coordinate_initialized_correctly(self):
        self.assertEqual((self.player.x, self.player.y), (500, 550))

    def test_points_increased_when_collision_happens(self):
        self.energy = PointCollector(500, 550)
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
        self.energy = PointCollector(500, 550)
        self.energy.obtainableposition()
        self.assertEqual(self.energy.x, 496)
