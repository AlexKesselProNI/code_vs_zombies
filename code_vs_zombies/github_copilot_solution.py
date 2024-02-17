import sys
import math

# game loop
while True:
    x, y = [int(i) for i in input().split()]
    human_count = int(input())
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
    zombie_count = int(input())
    zombies = []
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_x_next, zombie_y_next = [int(j) for j in input().split()]
        zombies.append((zombie_id, zombie_x, zombie_y, zombie_x_next, zombie_y_next))
    closest_zombie = min(zombies, key=lambda z: math.hypot(x - z[1], y - z[2]))
    print(f"{closest_zombie[1]} {closest_zombie[2]}")