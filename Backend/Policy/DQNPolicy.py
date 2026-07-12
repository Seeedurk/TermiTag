import torch 
import random
import numpy as np
from collections import deque
from Policy.QTrainer import QTrainer
import os

MAX_MEMORY = 500_000
BATCH_SIZE = 64
LR = 0.001

class DQNPolicy:
    #I need to figure out where to run train
    def __init__(self, model, state_size, action_size=4):
        self.n_games = 0
        self.epsilon = 0 #randomness, makes it so the AI actually does anything new
        self.gamma = 0.99 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = model
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

        #self.optimizer = torch.optim.Adam(self.model.parameters(), lr=LR)
        #self.criterion = torch.nn.MSELoss()

    def processWall(self, wall, runner_x, runner_y):
        if wall is None:
            return [0.0, 0.0, 0.0, 0.0]


        return [
            (wall.x - runner_x) / 800,
            (wall.y - runner_y) / 600,
            (wall.x + wall.width - runner_x) / 800, 
            (wall.y + wall.height - runner_y) / 600
        ]

    #Remember to change input size for model
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

        time_left = game.timeLeft

        distance_x = tagger_x - runner_x
        distance_y = tagger_y - runner_y
        left = runner_x / 800
        right = (800 - runner_x) / 800
        top = runner_y / 600
        bottom = (600 - runner_y) / 600

        nearestWall1 = nearestWall2 = None
        dist1 = dist2 = float("inf")
            
        for wall in game.Walls:
             
            closestX = max(wall.x, min(runner_x, wall.x + wall.width))
            closestY = max(wall.y, min(runner_y, wall.y + wall.height))

            dx = closestX - runner_x
            dy = closestY - runner_y

            distance = dx * dx + dy * dy

            if distance < dist1:
                nearestWall2 = nearestWall1
                nearestWall1 = wall

                dist2 = dist1
                dist1 = distance
            elif distance < dist2:
                nearestWall2 = wall
                dist2 = distance

        
        state = [
            runner_x / 800, runner_y / 600,
            runner_vx / 6, runner_vy / 6,
            tagger_x / 800, tagger_y / 600,
            tagger_vx / 6, tagger_vy / 6,
            distance_x / 800, distance_y / 600,     
            left, right, top, bottom,
            time_left / 10.0
        ]

        state.extend(self.processWall(nearestWall1, runner_x, runner_y))
        state.extend(self.processWall(nearestWall2, runner_x, runner_y))

        return np.array(state, dtype=float)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done);

    def train_long_memory(self):

        if len(self.memory) == 0:
            return

        if len(self.memory) > BATCH_SIZE:
            smaller_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            smaller_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*smaller_sample)

        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    def get_action(self, state):

        eps = max(0.05, 1.0 - self.n_games / 2000)

        state_tensor = torch.tensor(state, dtype=torch.float32)

        if random.random() < eps:
            return random.randint(0, 3)

        with torch.no_grad():
            qvals = self.model(state_tensor)

        return torch.argmax(qvals).item()

    def save(self, file='model.pth'):
        self.model.save(file)
        #print(self.n_games)
        metaData = {
            "n_games": self.n_games
            }
        torch.save(metaData, "./model/meta.pth")

    def load(self, file='model.pth'):
        self.model.load(file)
        meta_path = "./model/meta.pth"
        if os.path.exists(meta_path):
            meta = torch.load(meta_path)
            self.n_games = meta.get("n_games", 0)
            print(f"Loaded metadata: {self.n_games} episodes")
        else:
            print("No metadata found, starting with n_games = 0")



    def test(self):
        return;

    



