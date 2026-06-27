import eventlet
from Runner import Runner
from Tagger import Tagger
from Wall import Wall
import time
import math

class Game: #TODO: 
    def __init__(self):
        self.Mike = Runner(200, 300)
        self.Jason = Tagger(600,300)

        self.taggerScore = 0
        self.runnerScore = 0

        self.ended = False
        self.roundEnded = False;

        self.t0 =  time.time()
        self.timeLeft = 15;

        self.Walls = [Wall(400, 0, 20, 200), Wall(400, 400, 20, 200)]

    def timerReset(self):
        self.t0 = time.time()
        self.timerLeft = 10


    def checkTag(self):
       if(abs(self.Mike.retrieveX() - self.Jason.retrieveX()) < 20 and abs(self.Mike.retrieveY() - self.Jason.retrieveY()) < 20):
          print("You can't run lil bro")
          self.taggerScore += 1

          self.gameReset()
          return;

    def checkInBounds(self):
        if(self.Mike.retrieveX() > 800 or self.Mike.retrieveY() > 600 or self.Mike.retrieveX() < 0 or self.Mike.retrieveY() < 0):
            self.gameReset()
            self.taggerScore += 1
            return;

        if(self.Jason.retrieveX() > 800 or self.Jason.retrieveY() > 600 or self.Jason.retrieveX() < 0 or self.Jason.retrieveY() < 0):
            self.gameReset()
            self.runnerScore += 1
            return;

    def checkTimer(self):
        if(self.timeLeft <= 0):
            self.gameReset()
            self.runnerScore += 1
            return;
        
    def gameReset(self):
        self.Mike.roundReset();
        self.Jason.roundReset();
        self.timerReset()

    def checkWin(self):
        if(self.taggerScore >= 25):
            print("Tagger wins")
            self.ended = True
            return;
        if(self.runnerScore >= 25):
            print("Runner wins")
            self.ended = True
            return;

    def step(self, dt, action):
        #Set up game logic, use absolute value to see if runner is in range of tagger
        #Create random destruction objects that tagger and runner avoid
        #add function to both runner and tagger to get their own info, then a function to retrieve an actions 
        #In this step function


        if(self.ended == False):

            self.Mike.modelInput(action)
            self.Jason.basicTaggerAI(self.Mike.retrieveX(), self.Mike.retrieveY())

            self.Mike.update(dt)
            self.Jason.update(dt)
            self.checkTag()
            self.checkInBounds()
            self.checkTimer()
            self.checkWin()
            self.timeLeft = math.floor(10 - (time.time() - self.t0))
    
    def check_done(self):


        if(self.Mike.retrieveX() > 800 or self.Mike.retrieveY() > 600 or self.Mike.retrieveX() < 0 or self.Mike.retrieveY() < 0):
           return True;

        elif(self.Jason.retrieveX() > 800 or self.Jason.retrieveY() > 600 or self.Jason.retrieveX() < 0 or self.Jason.retrieveY() < 0):
           return True;

        elif(abs(self.Mike.retrieveX() - self.Jason.retrieveX()) < 20 and abs(self.Mike.retrieveY() - self.Jason.retrieveY()) < 20):
          return True;
        
        elif(self.timeLeft <= 0):
          return True;

        return False;

    def get_runnerReward(self): #TODO: Fully implement Tagger Reward
        rX = self.Mike.retrieveX()
        rY = self.Mike.retrieveY()
        tX = self.Jason.retrieveX()
        tY = self.Jason.retrieveY()

   
        rewardConst = 0.1

        reward = (abs(rX - tX) + abs(rY - tY)) * rewardConst

        reward += 1

        if(rX > 800 or rX < 0 or rY > 600 or rY < 0):
            reward -= 1000
  
        elif(abs(rX - tX) < 20 and abs(rY-tY) < 20):
            reward -= 500

        return reward;


    def train_step(self, action): 
        
        
        dt = 1/60

        self.Mike.modelInput(action)
        self.Jason.basicTaggerAI(self.Mike.retrieveX(), self.Mike.retrieveY())
        
        self.Mike.update(dt)
        self.Jason.update(dt)

        
        done = self.check_done()
        reward = self.get_runnerReward()

        return reward, done
            





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
            },
            'timer': {
                'time': self.timeLeft
            }
        }

