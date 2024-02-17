"""
Module: environment.environment

This module contains the CodeVSZombies class which simulates a game of Code vs Zombies.

Classes:
    CodeVSZombies: A class that represents a game of Code vs Zombies.
"""

import random
import numpy as np

# Constants
ARENA_WIDTH = 16000
ARENA_HEIGHT = 9000
ASH_SPEED = 1000
ASH_SHOOTING_RADIUS = 2000
ZOMBIE_SPEED = 400
ZOMBIE_KILLING_RADIUS = 400

class CodeVSZombies:
    def __init__(self, ash_x=None):
        self.ash = np.array([ash_x if ash_x is not None else random.randint(0, ARENA_WIDTH), 0])
        self.zombies = np.empty((0, 2), int)
        self.humans = np.empty((0, 2), int)
        self.score = 0
        self.fibonacci = np.array([1, 1])
        self.arena = np.zeros((ARENA_HEIGHT, ARENA_WIDTH))
         # Add random number of humans and zombies
        for _ in range(random.randint(1, 100)):
            self.add_human(random.randint(0, ARENA_WIDTH), random.randint(0, ARENA_HEIGHT))
        for _ in range(random.randint(1, 100)):
            self.add_zombie(random.randint(0, ARENA_WIDTH), random.randint(0, ARENA_HEIGHT))

    def add_zombie(self, x, y):
        self.zombies = np.append(self.zombies, np.array([[x, y]]), axis=0)

    def add_human(self, x, y):
        self.humans = np.append(self.humans, np.array([[x, y]]), axis=0)

    def move_ash(self, x, y):
        distance = np.linalg.norm([x - self.ash[0], y - self.ash[1]])
        if distance <= ASH_SPEED:
            self.ash = np.array([x, y])
        else:
            angle = np.arctan2(y - self.ash[1], x - self.ash[0])
            self.ash[0] += np.cos(angle) * ASH_SPEED
            self.ash[1] += np.sin(angle) * ASH_SPEED

    def move_zombies(self):
        for i in range(len(self.zombies)):
            distances = np.linalg.norm(self.humans - self.zombies[i], axis=1)
            target_index = np.argmin(distances)
            target = self.humans[target_index]
            distance = distances[target_index]
            if distance <= ZOMBIE_SPEED:
                self.zombies[i] = target
                if target in self.humans:
                    self.humans = np.delete(self.humans, target_index, 0)
            else:
                angle = np.arctan2(target[1] - self.zombies[i][1], target[0] - self.zombies[i][0])
                self.zombies[i][0] += np.cos(angle) * ZOMBIE_SPEED
                self.zombies[i][1] += np.sin(angle) * ZOMBIE_SPEED

    def shoot_zombies(self):
        distances = np.linalg.norm(self.zombies - self.ash, axis=1)
        killed_indices = np.where(distances <= ASH_SHOOTING_RADIUS)[0]
        for i, index in enumerate(killed_indices):
            while len(self.fibonacci) < i + 3:
                self.fibonacci = np.append(self.fibonacci, self.fibonacci[-1] + self.fibonacci[-2])
            self.score += (len(self.humans) ** 2) * 10 * self.fibonacci[i + 2]
        self.zombies = np.delete(self.zombies, killed_indices, 0)

    def game_over(self):
        return len(self.humans) == 0 or not (0 <= self.ash[0] < ARENA_WIDTH and 0 <= self.ash[1] < ARENA_HEIGHT)

    def play_turn(self, x, y):
        self.move_zombies()
        self.move_ash(x, y)
        self.shoot_zombies()
        return self.score

    def render(self):
        self.arena.fill(0)
        y, x = np.ogrid[-self.ash[1]:ARENA_HEIGHT-self.ash[1], -self.ash[0]:ARENA_WIDTH-self.ash[0]]
        mask = x*x + y*y <= ASH_SHOOTING_RADIUS**2
        self.arena[mask] = 1
        for zombie in self.zombies:
            y, x = np.ogrid[-zombie[1]:ARENA_HEIGHT-zombie[1], -zombie[0]:ARENA_WIDTH-zombie[0]]
            mask = x*x + y*y <= ZOMBIE_KILLING_RADIUS**2
            self.arena[mask] = -1
        for human in self.humans:
            self.arena[human[1], human[0]] = 2
        return self.arena