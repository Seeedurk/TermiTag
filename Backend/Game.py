import eventlet
from Runner import Runner
from Tagger import Tagger

class Game:
    def __init__(self):
        self.Mike = Runner(300, 300)
        self.Jason = Tagger(300,300)

    def checkTag(self):
        print(self.Mike.retrieveX())
        print(self.Mike.retrieveY())

    def step(self, dt):
        #Set up game logic, use absolute value to see if runner is in range of tagger
        #Create random destruction objects that tagger and runner avoid
        #add function to both runner and tagger to get their own info, then a function to retrieve an actions 
        #In this step function
        if(abs(self.Mike.retrieveX() - self.Jason.retrieveX()) < 20 and abs(self.Mike.retrieveY() - self.Jason.retrieveY()) < 20):
            print("You can't run lil bro")

        self.Mike.update(dt)
        self.Jason.update(dt)
        self.checkTag()
            
    def get_state(self):

        return [{'x': self.Mike.retrieveX(), 'y': self.Mike.retrieveY()}, {'x': self.Jason.retrieveX(), 'y': self.Jason.retrieveY()}]

