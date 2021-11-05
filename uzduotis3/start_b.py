import time
import exercise1.car_maze as cm

env = cm.CarMazeEnv()

#################################################
# Observation space value meanings by list index:
# 0 - up       (values: 0 - road blocked,  1 - road available)
# 1 - down
# 2 - left
# 3 - right
# 4 - ID position of car
# 5 - ID position of gold
#
###########################
# Action space values
# 0 - up
# 1 - down
# 2 - left
# 3 - right

#####################################
# You code starts here
#####################################

backtrack_count = 0


# Konvertuoti "x-y" į (x, y).
def point_to_tuple(point):
    p = point.split("-")
    return int(p[0]), int(p[1])


# Funkcija, kuri apskaičiuoja atstumą nuo taško A iki taško B
# pagal Manheteno atstumo metriką. d = |x1-x2|+|y1-y2|.
def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


# Funkcija, kuri suranda, kuris automobilio kaimyninis taškas
# iš neaplankytų taškų yra arčiausiai aukso.
# Jeigu nebėra neaplankytų taškų, grįžtama į ankstesnį, jau aplankytą tašką.
def neighbor_min_distance(point, neighbors, visited):
    global backtrack_count
    min_i = 0
    min_dist = float("inf")
    all_visited = True

    for i in range(0, len(neighbors)):
        if neighbors[i] not in visited:
            all_visited = False
            dist_i = manhattan_distance(point, neighbors[i])
            if dist_i < min_dist:
                min_i = i
                min_dist = dist_i

    # Skaičiuojama, kiek važiuoti atgal, jeigu nebėra neaplankytų taškų.
    # Jeigu atsiranda neaplankytų taškų, atgal važiuoti nebereikės, todėl
    # nustatomas nulis.
    if all_visited:
        backtrack_count += 2
    else:
        backtrack_count = 0

    return neighbors[min_i] if not all_visited else visited[-backtrack_count]


# Funkcija, kuri iš galimų veiksmų sudaro automobilio kaimyninių
# taškų sąrašą (į kuriuos taškus galima nuvažiuoti).
def get_neighbors(car, actions):
    neighbors = []

    for i in actions:
        neighbors.append((
            car[0] + (-1 if i == 2 else 1 if i == 3 else 0),
            car[1] + (-1 if i == 1 else 1 if i == 0 else 0)
        ))

    return neighbors


# Funkcija, kuri grąžina veiksmą pagal koordinačių poslinkį tarp dviejų taškų.
def get_action(point_a, point_b):
    x_shift, y_shift = point_b[0] - point_a[0], point_b[1] - point_a[1]

    if x_shift < 0:
        return 2
    if x_shift > 0:
        return 3
    if y_shift < 0:
        return 1
    if y_shift > 0:
        return 0


for i_episode in range(1):
    observation = env.reset()
    visited_path = []

    for t in range(200000):
        env.render()

        # --------------------------------------------
        # example code
        # --------------------------------------------
        # action = env.action_space.sample()

        time.sleep(0.1)
        avalableActions = [x[0] for x in enumerate(observation) if x[1] == 1]
        target = neighbor_min_distance(point_to_tuple(observation[5]),
                                       get_neighbors(point_to_tuple(observation[4]), avalableActions), visited_path)
        action = get_action(point_to_tuple(observation[4]), target)
        observation, reward, done, info = env.step(action)

        visited_path.append(point_to_tuple(observation[4]))

        if done:
            print("Episode finished after {} timesteps".format(t + 1))
            print("Reward - " + str(reward))
            break

        # --------------------------------------------
        # end of example code
        # --------------------------------------------

#####################################
# You code ends here
#####################################


env.close()
