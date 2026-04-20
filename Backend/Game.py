import eventlet
from Runner import Runner
from Tagger import Tagger

class Game:
    def __init__(self):
        self.Mike = Runner(300, 300)
        self.Jason = Tagger(300,300)

    def checkTag(self):
       if(abs(self.Mike.retrieveX() - self.Jason.retrieveX()) < 20 and abs(self.Mike.retrieveY() - self.Jason.retrieveY()) < 20):
          print("You can't run lil bro")
          self.Mike.modifyX(100)
          self.Mike.modifyY(200)

    def checkInBounds(self):
        if(self.Mike.retrieveX() > 600 or self.Mike.retrieveY() > 800 or self.Mike.retrieveX() < 0 or self.Mike.retrieveY() < 0):
            self.Mike.modifyY(100)
            self.Mike.modifyX(200)

    def step(self, dt):
        #Set up game logic, use absolute value to see if runner is in range of tagger
        #Create random destruction objects that tagger and runner avoid
        #add function to both runner and tagger to get their own info, then a function to retrieve an actions 
        #In this step function



        self.Mike.update(dt)
        self.Jason.update(dt)
        self.checkTag()
        self.checkInBounds()
            
    def get_state(self):

        return [{'x': self.Mike.retrieveX(), 'y': self.Mike.retrieveY()}, {'x': self.Jason.retrieveX(), 'y': self.Jason.retrieveY()}]

