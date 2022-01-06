import gym
import car_maze as cm
import dqn_car_agent as dqn
import random as rnd
import numpy as np
import time

env = cm.CarMazeEnv()
agent = dqn.DQNCarAgent(env)
batch_size = 16


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

# Pakeisti būsenos formatą
def convert_state(s):
    p1 = s[4].split("-")
    p2 = s[5].split("-")
    return [s[0], s[1], s[2], s[3], int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])]


# Funkcija, kuri apskaičiuoja atstumą nuo taško A iki taško B
# pagal Manheteno atstumo metriką. d = |x1-x2|+|y1-y2|.
# Atstumas bus naudojamas kaip atlygis - kuo mažesnis atstumas,
# tuo didesnį atlygį gaus agentas.
def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


for i_episode in range(50):
    state = env.reset()
    state = convert_state(state)
    # state = np.reshape(state, [1, 6])
    print(state)

    visited = set()

    for t in range(200000):
        env.render()

        # # --------------------------------------------
        # # example code
        # # --------------------------------------------

        # time.sleep(0.01)

        # Nurodyti agentui veiksmą.
        # Jeigu RAND <= EPSILON, tada bus vykdomas atsitiktinis veiksmas,
        # o jeigu ne, tada bus imama didžiausia reikšmė.
        # available_actions = [x[0] for x in enumerate(state[0][:4]) if x[1] == 1]
        available_actions = [x[0] for x in enumerate(state[:4]) if x[1] == 1]
        action = agent.act(state, available_actions)

        next_state, reward, done, info = env.step(action)
        next_state = convert_state(next_state)
        # next_state = np.reshape(next_state, [1, 6])
        # print(observation[6])

        # Stebėti aplankytus taškus
        visited.add((state[4:][0], state[4:][1]))

        # Atlygis atvirkščiai proporcingas atstumui
        total_reward = 1 / (1 + manhattan_distance((next_state[4:][0], next_state[4:][1]),
                                                   (next_state[4:][2], next_state[4:][3])))

        # Mažinti alygį, jeigu automobilis važiuoja į anksčiau aplankytą tąšką
        if (next_state[4:][0], next_state[4:][1]) in visited:
            total_reward *= 0.66

        # Atsižvelgti į atlygį iš aplinkos būsenos
        total_reward *= 0.5 if reward < 0 else 1.5

        # Nurodyti agentui, kad įsimintų būseną, veiksmus ir atlygį.
        agent.remember(state, action, total_reward, next_state, done)

        # Būsenos atnaujinimas
        state = next_state

        # Mokyti agentą
        agent.replay(batch_size)

        # Keičiama Epsilon reikšmė
        agent.adaptive_e_greedy()

        if done:
            print("Episode finished after {} timesteps".format(t + 1))
            print("Reward - {}".format(total_reward))
            break

        # # --------------------------------------------
        # # end of example code
        # # --------------------------------------------

#####################################
# You code ends here
#####################################

env.close()
