"""
Module: tests.environment_tests

This module contains the TestCodeVSZombies class which tests the CodeVSZombies class from the environment.environment module.

Classes:
    TestCodeVSZombies: A class that tests the CodeVSZombies class.
"""

import unittest
import numpy as np
import sys
sys.path.append('../code_vs_zombies/')

from environment.environment import CodeVSZombies

# Constants
ARENA_WIDTH = 16000
ARENA_HEIGHT = 9000
ASH_SPEED = 1000
ASH_SHOOTING_RADIUS = 2000
ZOMBIE_SPEED = 400
ZOMBIE_KILLING_RADIUS = 400

class TestCodeVSZombies(unittest.TestCase):
    def setUp(self):
        self.game = CodeVSZombies()

    def test_add_zombie(self):
        self.game.add_zombie(5000, 5000)
        self.assertTrue((self.game.zombies == np.array([[5000, 5000]])).all())

    def test_add_human(self):
        self.game.add_human(5000, 5000)
        self.assertTrue((self.game.humans == np.array([[5000, 5000]])).all())

    def test_move_ash(self):
        self.game.move_ash(5000, 5000)
        self.assertTrue((self.game.ash == np.array([5000, 5000])).all())

    def test_move_zombies(self):
        self.game.add_zombie(5000, 5000)
        self.game.add_human(6000, 6000)
        self.game.move_zombies()
        self.assertTrue((self.game.zombies[0] != np.array([5000, 5000])).any())

    def test_shoot_zombies(self):
        self.game.add_zombie(5000, 5000)
        self.game.move_ash(5000, 5000)
        self.game.shoot_zombies()
        self.assertEqual(len(self.game.zombies), 0)

    def test_game_over(self):
        self.assertFalse(self.game.game_over())
        self.game.ash = np.array([-1, -1])
        self.assertTrue(self.game.game_over())

    def test_play_turn(self):
        self.game.add_zombie(5000, 5000)
        score = self.game.play_turn(5000, 5000)
        self.assertEqual(score, 10)

    def test_render(self):
        self.game.add_zombie(5000, 5000)
        self.game.add_human(6000, 6000)
        self.game.move_ash(4000, 4000)
        arena = self.game.render()

        # Check all points inside circle around Ash
        y, x = np.ogrid[-self.game.ash[1]:ARENA_HEIGHT-self.game.ash[1], -self.game.ash[0]:ARENA_WIDTH-self.game.ash[0]]
        mask = x*x + y*y <= ASH_SHOOTING_RADIUS**2
        self.assertTrue((arena[mask] == 1).all())

        # Check all points inside circles around zombies
        for zombie in self.game.zombies:
            y, x = np.ogrid[-zombie[1]:ARENA_HEIGHT-zombie[1], -zombie[0]:ARENA_WIDTH-zombie[0]]
            mask = x*x + y*y <= ZOMBIE_KILLING_RADIUS**2
            self.assertTrue((arena[mask] == -1).all())

        # Check all points of humans
        for human in self.game.humans:
            self.assertEqual(arena[human[1], human[0]], 2)

if __name__ == '__main__':
    unittest.main()