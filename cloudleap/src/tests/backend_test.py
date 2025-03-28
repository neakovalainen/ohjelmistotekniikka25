import unittest
from backendleap import InitializeGame, Meow, PointCollector

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.player = Meow(500, 550)

    def test_player_x_coordinate_initialized_correctly(self):
        self.assertEqual((self.player.x, self.player.y), (500, 550))

    def test_points_increased_when_collision_happens(self):
        self.energy = PointCollector(500, 550)
        self.energy.collision_detector(self.player, self.energy)
        self.assertEqual(self.energy.points, 1)