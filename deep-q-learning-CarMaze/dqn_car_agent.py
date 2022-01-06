import random
from collections import deque

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam


class DQNCarAgent:
    def __init__(self, env):
        # Būsenų skaičius (neuroninio tinklo įvestis)
        self.state_size = 8
        # Veiksmų skaičius (neuroninio tinklo išvestis)
        self.action_size = env.action_space.n

        # Gamma kontroliuoja atlygio įtaką tolimesniuose etapuose
        self.gamma = 0.95
        self.learning_rate = 0.001

        # Čia nustatoma pradinė Epsilon reikšmė, kokiu greičiu reikia
        # keisti ją ir kokia gali būti minimali jos reikšmė.
        self.epsilon = 1
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        # Atmintis su ribotu dydžiu. Kai dydis bus viršytas,
        # pirmieji elementai bus pašalinami.
        self.memory = deque(maxlen=1000)

        self.model = self.build_model()

    # Funkcija, kuri sudaro neuroninį tinklą giliajam Q mokymuisi.
    def build_model(self):
        model = Sequential()
        model.add(Dense(48, input_dim=self.state_size, activation='tanh'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    # Įrašymas į atmintį
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((tf.reshape(state, [1, self.state_size]), action, reward,
                            tf.reshape(next_state, [1, self.state_size]), done))

    # Funkcija, kuri nurodo agentui, ką jam daryti.
    # Jeigu RAND <= EPSILON, tada bus vykdomas atsitiktinis veiksmas,
    # o jeigu ne, tada bus imama didžiausia reikšmė.
    def act(self, state, available_actions):
        if random.uniform(0, 1) <= self.epsilon:
            return available_actions[random.randint(0, len(available_actions) - 1)]
        else:
            act_values = self.model.predict(tf.reshape(state, [1, self.state_size]))
            return np.argmax(act_values[0])

    # Funkcija, skirta neuroninio tinklo mokymui
    def replay(self, batch_size):
        # Jeigu nepakanka elementų atmintyje, tada nieko nedaryti
        if len(self.memory) < batch_size:
            return None

        # Atsitiktinai paimama `batch_size` elementų iš atminties
        subset = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in subset:
            if not done:
                # target = R(s,a) + gamma * maxQ`(s`,a`)
                # target (maxQ` reikšmė) yra neuroninio tinklo išvestis, kai s` yra įvestis
                # amax(): paima didžiausią elementą iš sąrašo
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
                train_target = self.model.predict(state)
                train_target[0][action] = target
                # Galima nustatyti verbose=1, kad rodyti neuroninio tinklo mokymo informaciją
                self.model.fit(state, train_target, verbose=0)

    # Funkcija, kurią įvykdžius sumažėja Epsilon reikšmė pagal nurodytą greitį.
    def adaptive_e_greedy(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
