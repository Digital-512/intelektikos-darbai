import numpy as np

import cartpole_env as cm
import dqn_agent as dqn

env = cm.CartPoleEnv()
agent = dqn.DQNAgent(env)
batch_size = 16

for i_episode in range(50):
    state = env.reset()
    state = np.reshape(state, [1, 4])

    # Kiekvieną kartą agentas gaus atlygį (reward).
    # Kuo ilgiau išsilaikys, tuo didesnį atlygį sukaups.
    for t in range(10000):
        env.render()

        # time.sleep(0.01)

        # Nurodyti agentui veiksmą.
        # Jeigu RAND <= EPSILON, tada bus vykdomas atsitiktinis veiksmas,
        # o jeigu ne, tada bus imama didžiausia reikšmė.
        action = agent.act(state, env)

        # Vykdyti kitą žingsnį
        next_state, reward, done, info = env.step(action)
        next_state = np.reshape(next_state, [1, 4])

        # Nurodyti agentui, kad įsimintų būseną, veiksmus ir atlygį.
        agent.remember(state, action, reward, next_state, done)

        # Būsenos atnaujinimas
        state = next_state

        # Mokyti agentą
        agent.replay(batch_size)

        # Keičiama Epsilon reikšmė
        agent.adaptive_e_greedy()

        if done:
            print("Episode: {}, Time: {}".format(i_episode, t))
            break

env.close()
