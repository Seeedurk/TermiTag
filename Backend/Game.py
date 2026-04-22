import eventlet
from Runner import Runner
from Tagger import Tagger
from Wall import Wall

class Game:
    def __init__(self):
        self.Mike = Runner(200, 300)
        self.Jason = Tagger(600,300)

        self.taggerScore = 0
        self.runnerScore = 0

        self.ended = False

        self.Walls = [Wall(400, 0, 20, 200), Wall(400, 400, 20, 200)]


    def checkTag(self):
       if(abs(self.Mike.retrieveX() - self.Jason.retrieveX()) < 20 and abs(self.Mike.retrieveY() - self.Jason.retrieveY()) < 20):
          print("You can't run lil bro")
          self.taggerScore += 1

          self.Mike.roundReset();
          self.Jason.roundReset();
          return;

    def checkInBounds(self):
        if(self.Mike.retrieveX() > 800 or self.Mike.retrieveY() > 600 or self.Mike.retrieveX() < 0 or self.Mike.retrieveY() < 0):
            self.Mike.roundReset();
            self.Jason.roundReset();
            self.taggerScore += 1
            return;

        if(self.Jason.retrieveX() > 800 or self.Jason.retrieveY() > 600 or self.Jason.retrieveX() < 0 or self.Jason.retrieveY() < 0):
            self.Mike.roundReset();
            self.Jason.roundReset();
            self.runnerScore += 1
            return;

    def checkWin(self):
        if(self.taggerScore >= 5):
            print("Tagger wins")
            self.ended = True
            return;
        if(self.runnerScore >= 5):
            print("Runner wins")
            self.ended = True
            return;

    def step(self, dt):
        #Set up game logic, use absolute value to see if runner is in range of tagger
        #Create random destruction objects that tagger and runner avoid
        #add function to both runner and tagger to get their own info, then a function to retrieve an actions 
        #In this step function


        if(self.ended == False):
            self.Mike.update(dt)
            self.Jason.update(dt)
            self.checkTag()
            self.checkInBounds()
            self.checkWin()
            
    def get_state(self):

        walls_data = [
            {'x': wall.x, 'y': wall.y, 'width': wall.width, 'height': wall.height} 
            for wall in self.Walls
        ]
        #Add score object that is sent along side the positional data
        return {
            'runner': {
                'x': self.Mike.retrieveX(), 
                'y': self.Mike.retrieveY()
            }, 
            'tagger': {
                'x': self.Jason.retrieveX(), 
                'y': self.Jason.retrieveY()
            }, 
            'scores': {
                'taggerScore': self.taggerScore, 
                'runnerScore': self.runnerScore
            }
        }

