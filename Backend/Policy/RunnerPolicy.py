import torch 
import random
import numpy as np
from collections import deque


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class RunnerPolicy:
    #I need to figure out where to run train
    def __init__(self, state, reward, done):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)

        self.state = state
        self.reward = reward
        self.done = done


    def get_state(self, game):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def remember(self, actions):
        pass

    def get_action(self, state):
        pass

    def train():
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0

        while True:
            state_old = RunnerPolicy.get_state()
        #I have to use data that is passed down from the runner and then game

    



