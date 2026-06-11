import torch 
import random
import numpy as np
from collections import deque


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class RunnerPolicy:
    #I need to figure out where to run train
    def __init__(self, model, state_size, action_size=4):
        self.n_games = 0
        self.epsilon = 0 #randomness, makes it so the AI actually does anything new
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = model;
        #self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

        #self.optimizer = torch.optim.Adam(self.model.parameters(), lr=LR)
        #self.criterion = torch.nn.MSELoss()

    def get_state(self, game):
        runner = game.Mike
        tagger = game.Jason

        runner_x = runner.retrieveX()
        runner_y = runner.retrieveY()
        runner_vx = runner.deltaX
        runner_vy = runner.deltaY

        tagger_x = tagger.retrieveX()
        tagger_y = tagger.retrieveY()
        tagger_vx = tagger.deltaX
        tagger_vy = tagger.deltaY

        distance_x = tagger_x - runner_x
        distance_y = tagger_y - runner_y

        state = [
            runner_x,
            runner_y,
            runner_vx,
            runner_vy,
            tagger_x,
            tagger_y,
            tagger_vx,
            tagger_vy,
            distance_x,
            distance_y
        ]

        return np.array(state, dtype=float)


    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    def get_action(self, state):
        return 0;

    def train():
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0

        while True:
            state_old = RunnerPolicy.get_state()
        #I have to use data that is passed down from the runner and then game

    def test(self):
        return;

    



