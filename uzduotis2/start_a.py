import time
import exercise1.car_maze as cm
import exercise1.graph as g

env = cm.CarMazeEnv("open")


#################################################
# Observation space value meanings by list index:
# 0 - up       (values: 0 - road blocked,  1 - road available)
# 1 - down
# 2 - left
# 3 - right
# 4 - ID position of car
# 5 - ID position of gold
# 6 - roads / possible moves of the maze. Tuple of two ID values (from, to)
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

# Funkcija, kuri sudaro veiksmų seką iš trumpiausio kelio sekos
def get_actions(path):
    last_x, last_y = path[0].split("-")
    last_x = int(last_x)
    last_y = int(last_y)
    action_sequence = []

    for i in range(1, len(path)):
        x, y = path[i].split("-")
        x = int(x)
        y = int(y)
        if last_x < x:
            action_sequence.append(3)
        if last_x > x:
            action_sequence.append(2)
        if last_y < y:
            action_sequence.append(0)
        if last_y > y:
            action_sequence.append(1)
        last_x = x
        last_y = y

    return action_sequence


for i_episode in range(1):
    graph = g.Graph()
    observation = env.reset()

    # Užpildyti grafą
    # Briaunų sąrašas konvertuojamas į gretimumo sąrašą
    for edge in observation[6]:
        graph.add_edge(edge[0], edge[1])

    shortest_path = graph.shortest_path(observation[4], observation[5])
    actions = get_actions(shortest_path)

    print(shortest_path)
    print(actions)

    for t in actions:
        env.render()

        # --------------------------------------------
        # example code
        # --------------------------------------------
        # action = env.action_space.sample()

        time.sleep(0.3)
        observation, reward, done, info = env.step(t)

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
