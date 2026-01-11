import eventlet
from Runner import Runner
from Tagger import Tagger

class Game:
    def __init__(self):
        self.Mike = Runner(10, 10)
        self.Jason = Tagger(20,20)

    def step(self, dt):
        self.Mike.update(100, 100, dt)
            
    def get_state(self):
        return {'x': self.Mike.retrieveX(), 'y': self.Mike.retrieveY()}

