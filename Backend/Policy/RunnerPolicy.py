class RunnerPolicy:
    def __init__(self, state, reward, done):
        self.state = state
        self.reward = reward
        self.done = done

    def remember(self, actions):
        pass

    def action(self, state, actions, reward):
        pass

