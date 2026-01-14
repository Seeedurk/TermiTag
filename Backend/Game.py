import eventlet
from Runner import Runner
from Tagger import Tagger

class Game:
    def __init__(self):
        self.Mike = Runner(300, 300)
        self.Jason = Tagger(20,20, 0, 0)

    def step(self, dt):
        self.Mike.update(dt)
            
    def get_state(self):
        return [{'x': self.Mike.retrieveX(), 'y': self.Mike.retrieveY()}, {'x': self.Jason.retrieveX(), 'y': self.Jason.retrieveY()}]

