import sys
import math
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN


ASH_SPEED = 1000
ASH_SHOOTING_RADIUS = 2000
ZOMBIE_SPEED = 400
ZOMBIE_KILL_RADIUS = 400

def calculate_interception_point(zombie_x, zombie_y, zombie_to_x, zombie_to_y, ash_x, ash_y, ash_speed):
    dx = zombie_to_x - zombie_x
    dy = zombie_to_y - zombie_y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    time = distance / ZOMBIE_SPEED
    ash_distance = time * ASH_SPEED
    ash_dx = ash_x - zombie_x
    ash_dy = ash_y - zombie_y
    ash_distance_ratio = ash_distance / distance
    interception_x = zombie_x + dx * ash_distance_ratio
    interception_y = zombie_y + dy * ash_distance_ratio
    interception_x = max(0, interception_x)
    interception_x = min(16000, interception_x)
    interception_y = max(0, interception_y)
    interception_y = min(9000, interception_y)
    return interception_x, interception_y

while True:
    x, y = [int(i) for i in input().split()]
    print('Ash:', file=sys.stderr, flush=True)
    print(x, y, file=sys.stderr, flush=True)

    human_count = int(input())
    humans={
        'x': [],
        'y': []
    }
    for _ in range(human_count):
        _, x, y = map(int, input().split())
        humans['x']+=[x]
        humans['y']+=[y]
    humans_df = pd.DataFrame(humans)
    dbscan_humans = DBSCAN(eps=ASH_SHOOTING_RADIUS, min_samples=1).fit(humans_df)
    humans_df['cluster'] = dbscan_humans.labels_
    humans_df['c_x'] = humans_df['cluster'].map(lambda z: np.mean(humans_df[humans_df['cluster'] == z]['x']))
    humans_df['c_y'] = humans_df['cluster'].map(lambda z: np.mean(humans_df[humans_df['cluster'] == z]['y']))
    vc = humans_df['cluster'].value_counts()
    humans_df['cluster_size'] = humans_df['cluster'].map(lambda z: vc[z])

    zombie_count = int(input())
    zombies={
        'x': [],
        'y': [],
        'to_x': [],
        'to_y': []
    }
    for i in range(zombie_count):
        _, x, y, to_x, to_y = map(int, input().split())
        zombies['x'].append(x)
        zombies['y'].append(y)
        zombies['to_x'].append(to_x)
        zombies['to_y'].append(to_y)

    zombies_df=pd.DataFrame(zombies)
    print('All zombies:', file=sys.stderr, flush=True)
    print(zombies_df, file=sys.stderr, flush=True)

    for i in range(zombie_count):
            zombie_x = zombies_df.loc[i, 'x']
            zombie_y = zombies_df.loc[i, 'y']
            zombie_to_x = zombies_df.loc[i, 'to_x']
            zombie_to_y = zombies_df.loc[i, 'to_y']
            interception_x, interception_y = calculate_interception_point(zombie_x, zombie_y, zombie_to_x, zombie_to_y, x, y, ASH_SPEED)
            zombies_df.loc[i, 'interception_x'] = interception_x
            zombies_df.loc[i, 'interception_y'] = interception_y

    print('All zombies:', file=sys.stderr, flush=True)
    print(zombies_df, file=sys.stderr, flush=True)

    dbscan_zombies = DBSCAN(eps=ZOMBIE_KILL_RADIUS*2, min_samples=1).fit(zombies_df.drop(columns=['to_x', 'to_y']))
    zombies_df['cluster'] = dbscan_zombies.labels_
    zombies_df['c_x'] = zombies_df['cluster'].map(lambda x: np.mean(zombies_df[zombies_df['cluster'] == x]['x']))
    zombies_df['c_y'] = zombies_df['cluster'].map(lambda x: np.mean(zombies_df[zombies_df['cluster'] == x]['y']))
    vc = zombies_df['cluster'].value_counts()
    zombies_df['cluster_size'] = zombies_df['cluster'].map(lambda z: vc[z])

    for i in range(human_count):
        distances = np.sqrt((humans_df.loc[i, 'x'] - zombies_df['x']) ** 2 +
                            (humans_df.loc[i, 'y'] - zombies_df['y']) ** 2)
        humans_df.loc[i, 'distance_to_nearest_zombie'] = distances.min()
        humans_df.loc[i, 'nearest_zombie'] = distances.idxmin()

    humans_df['nearest_zombie_cluster_size'] = zombies_df.loc[humans_df['nearest_zombie'], 'cluster_size'].values
    humans_df['dead_time'] = (humans_df['distance_to_nearest_zombie'] - ZOMBIE_KILL_RADIUS) / ZOMBIE_SPEED
    humans_df['ash_x'] = x
    humans_df['ash_y'] = y
    humans_df['save_time'] = (np.sqrt((humans_df['x'] - humans_df['ash_x']) ** 2 + (humans_df['x'] - humans_df['ash_x']) ** 2) - ASH_SHOOTING_RADIUS) / ASH_SPEED
    print('All humans:', file=sys.stderr, flush=True)
    print(humans_df, file=sys.stderr, flush=True)
    humans_df.reset_index(drop=True, inplace=True)

    if humans_df.empty:
        print(x, y) # Stop Ash
    else:
        humans_we_can_save = humans_df[humans_df['save_time'] > humans_df['dead_time']]
        if humans_we_can_save.empty:
            humans_df = humans_df.sort_values(by=['save_time', 'cluster_size', 'nearest_zombie_cluster_size' ], ascending=[True, False, False])
            human_to_save = humans_df.index[0]
        else:
            humans_df = humans_we_can_save.sort_values(by=['save_time', 'cluster_size', 'nearest_zombie_cluster_size' ], ascending=[False, False, False])
            human_to_save = humans_df.index[0]

        to_x = zombies_df.loc[humans_df.loc[human_to_save, 'nearest_zombie'], 'interception_x']
        to_y = zombies_df.loc[humans_df.loc[human_to_save, 'nearest_zombie'], 'interception_y']

        print('Humans we can save:', file=sys.stderr, flush=True)
        print(humans_df, file=sys.stderr, flush=True)
        print(f"{to_x:.0f} {to_y:.0f}")