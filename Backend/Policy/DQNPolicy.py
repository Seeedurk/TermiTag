import torch 
import random
import numpy as np
from collections import deque
from Policy.QTrainer import QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class DQNPolicy:
    #I need to figure out where to run train
    def __init__(self, model, state_size, action_size=4):
        self.n_games = 0
        self.epsilon = 0 #randomness, makes it so the AI actually does anything new
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = model
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

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
        self.trainer.train_step(state, action, reward, next_state, done);

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            smaller_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            smaller_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*smaller_sample)

        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    def get_action(self, state):
        self.epsilon = max(5, 250 - self.n_games)

        state_tensor = torch.tensor(state, dtype=torch.float32)
        if(random.randint(0, 200) < self.epsilon):
            action = random.randint(0,3)
            return action

        QVals = self.model(state_tensor)
        action = torch.argmax(QVals).item()
        return action

    def save(self, file='model.pth'):
        self.model.save(file)

    def load(self, file='model.pth'):
        self.model.load(file)


    def test(self):
        return;

    



