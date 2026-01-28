class RunnerPolicy:
    def __init__(self, state, reward, done):
        self.state = state
        self.reward = reward
        self.done = done

    def remember(self, actions):
        pass

    def action(self, state, actions, reward):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass


