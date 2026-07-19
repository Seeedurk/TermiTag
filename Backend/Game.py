import eventlet
from Runner import Runner
from Tagger import Tagger
from Wall import Wall
import random
import time
import math

class Game: #TODO: 
    def __init__(self):
        self.Mike = Runner(100, 300)
        self.Jason = Tagger(700,300)

        self.taggerScore = 0
        self.runnerScore = 0

        self.ended = False
        self.roundEnded = False;

        self.t0 =  time.time()
        self.timeLeft = 10;

        
        self.Walls = [Wall(400, 0, 20, 200), Wall(400, 400, 20, 200)]
        #self.Walls = [Wall(400, 300, 100, 100)]

        self.total_movement = 0.0

        self.prev_potential = self._current_potential()

        self.reward_components = {"potential": 0.0, "terminal": 0.0}

    def timerReset(self):
        self.t0 = time.time()
        self.timeLeft = 10


    def checkTag(self):
       if(abs(self.Mike.retrieveX() - self.Jason.retrieveX()) < 20 and abs(self.Mike.retrieveY() - self.Jason.retrieveY()) < 20):
          self.taggerScore += 1

          self.gameReset()
          return;

    def checkInBounds(self):
        rX, rY = self.Mike.retrieveX(), self.Mike.retrieveY()
        tX, tY = self.Jason.retrieveX(), self.Jason.retrieveY()
        if(rX > 800 or rX < 0 or rY > 600 or rY < 0):
            self.gameReset()
            self.taggerScore += 1
            return;

        if(tX > 800 or tX < 0 or tY > 600 or tY < 0):
            self.gameReset()
            self.runnerScore += 1
            return;

    def checkTimer(self):
        if(self.timeLeft <= 0):
            self.gameReset()
            self.runnerScore += 1
            return;
        
    def gameReset(self):
        self.total_movement = 0.0
        self.Mike.roundReset();
        self.Jason.roundReset();
        self.timerReset()
        self.createWalls(random.randint(0, 5));
        self.prev_potential = self._current_potential()
        self.reward_components = {"potential": 0.0, "terminal": 0.0}

    def checkWin(self):
        if(self.taggerScore >= 25):
            print("Tagger wins")
            self.ended = True
            return;
        if(self.runnerScore >= 25):
            print("Runner wins")
            self.ended = True
            return;

    def createWalls(self, number):
        self.Walls = []
        for i in range(number):
            x = random.randint(150, 500)
            y = random.randint(100, 500)
            width = random.randint(50, 150)
            height = random.randint(50, 150)

            self.Walls.append(Wall(x, y, width, height))

    def checkWalls(self):
        for wall in self.Walls:
            if(self.Mike.retrieveX() >= wall.x and self.Mike.retrieveX() <= (wall.x + wall.width) 
               and self.Mike.retrieveY() >= wall.y and self.Mike.retrieveY() <= wall.y + wall.height):
                self.gameReset()
                self.taggerScore += 1
                return;
            elif (self.Jason.retrieveX() >= wall.x and self.Jason.retrieveX() <= (wall.x + wall.width) 
               and self.Jason.retrieveY() >= wall.y and self.Jason.retrieveY() <= wall.y + wall.height):
                self.gameReset()
                self.runnerScore += 1
                return;
        
  
    def step(self, dt, action):
        #Set up game logic, use absolute value to see if runner is in range of tagger
        #Create random destruction objects that tagger and runner avoid
        #add function to both runner and tagger to get their own info, then a function to retrieve an actions 
        #In this step function


        if(self.ended == False):

            self.Mike.modelInput(action)
            self.Jason.basicTaggerAI(self.Mike.retrieveX(), self.Mike.retrieveY(), self.Walls)

            self.Mike.update(dt)
            self.Jason.update(dt)
            self.checkTag()
            self.checkInBounds()
            self.checkWalls()
            self.checkTimer()
            self.checkWin()
            self.timeLeft = math.floor(10 - (time.time() - self.t0))
    
    def check_done(self):
        rX, rY = self.Mike.retrieveX(), self.Mike.retrieveY()
        tX, tY = self.Jason.retrieveX(), self.Jason.retrieveY()


        if(self.Mike.retrieveX() > 800 or self.Mike.retrieveY() > 600 or self.Mike.retrieveX() < 0 or self.Mike.retrieveY() < 0):
           return True

        elif(self.Jason.retrieveX() > 800 or self.Jason.retrieveY() > 600 or self.Jason.retrieveX() < 0 or self.Jason.retrieveY() < 0):
           return True

        elif(math.hypot(rX - tX, rY - tY) < 20):
          return True
        
        elif(self.timeLeft <= 0):
          return True

        for wall in self.Walls:
            if(self.Mike.retrieveX() >= wall.x and self.Mike.retrieveX() <= (wall.x + wall.width) 
               and self.Mike.retrieveY() >= wall.y and self.Mike.retrieveY() <= wall.y + wall.height):
               return True
            elif (self.Jason.retrieveX() >= wall.x and self.Jason.retrieveX() <= (wall.x + wall.width) 
               and self.Jason.retrieveY() >= wall.y and self.Jason.retrieveY() <= wall.y + wall.height):
               return True

        return False

    def _current_potential(self):
        rX, rY = self.Mike.retrieveX(), self.Mike.retrieveY()
        tX, tY = self.Jason.retrieveX(), self.Jason.retrieveY()
        dist = math.hypot(rX - tX, rY - tY)
        tagger_score = min(dist, 300.0) / 300.0
        margin = min(rX, 800 - rX, rY, 600 - rY)
        edge_danger = max(0.0, (80 - margin) / 80)
        wall_margin = min(
            (math.hypot(rX - max(w.x, min(rX, w.x+w.width)), rY - max(w.y, min(rY, w.y+w.height))))
            for w in self.Walls
        ) if self.Walls else 999
        wall_danger = max(0.0, (60 - wall_margin) / 60)
        return tagger_score - max(edge_danger, wall_danger)

    

    def get_runnerReward(self):
        rX, rY = self.Mike.retrieveX(), self.Mike.retrieveY()
        tX, tY = self.Jason.retrieveX(), self.Jason.retrieveY()
        dist = math.hypot(rX - tX, rY - tY)

        # ---- Terminal outcomes: one consistent magnitude, checked first ----
        if rX > 800 or rX < 0 or rY > 600 or rY < 0:
            self.reward_components["terminal"] += -30
            return -30
        if dist < 20:
            self.reward_components["terminal"] += -30
            return -30
        if self.timeLeft <= 0:
            self.reward_components["terminal"] += 30
            return 30
        if tX > 800 or tX < 0 or tY > 600 or tY < 0:
            self.reward_components["terminal"] += 30
            return 30
        for wall in self.Walls:
            if rX >= wall.x and rX <= wall.x + wall.width and rY >= wall.y and rY <= wall.y + wall.height:
                self.reward_components["terminal"] += -30
                return -30
            elif tX >= wall.x and tX <= wall.x + wall.width and tY >= wall.y and tY <= wall.y + wall.height:
                self.reward_components["terminal"] += 30
                return 30

        # ---- Potential function: single "how safe is this position" score, roughly [-1, 1] ----
        # Ng, Harada & Russell (1999): shaping of the form gamma*Phi(s') - Phi(s) preserves
        # the optimal policy while densifying the reward signal. Because it telescopes across
        # a trajectory, it cannot accumulate unboundedly with episode length the way independent
        # per-frame terms (old delta/edge/wall) did.
        SAFE_DIST = 300.0
        tagger_score = min(dist, SAFE_DIST) / SAFE_DIST  # 0 (on top of tagger) to 1 (far away)

        margin = min(rX, 800 - rX, rY, 600 - rY)
        edge_threshold = 80
        edge_danger = max(0.0, (edge_threshold - margin) / edge_threshold)  # 0 to 1

        wall_margin = min(
            (math.hypot(rX - max(w.x, min(rX, w.x + w.width)), rY - max(w.y, min(rY, w.y + w.height))))
            for w in self.Walls
        ) if self.Walls else 999
        wall_threshold = 60
        wall_danger = max(0.0, (wall_threshold - wall_margin) / wall_threshold)  # 0 to 1

        hazard = max(edge_danger, wall_danger)  # worse of the two, don't stack them
        new_potential = tagger_score - hazard   # roughly [-1, 1]: high = safe & far, low = in danger

        GAMMA = self.Mike.policy.gamma  # match the agent's own discount factor, per the PBRS formula
        SHAPING_SCALE = 10.0            # single tunable knob controlling shaping magnitude

        shaping_reward = (GAMMA * new_potential - self.prev_potential) * SHAPING_SCALE
        self.prev_potential = new_potential

        self.reward_components["potential"] += shaping_reward

        return max(-5, min(5, shaping_reward))


    def train_step(self, action): 
        
        
        dt = 1/60

        self.Mike.modelInput(action)
        self.Jason.basicTaggerAI(self.Mike.retrieveX(), self.Mike.retrieveY(), self.Walls)
        
        self.Mike.update(dt)

        self.total_movement += abs(self.Mike.deltaX) + abs(self.Mike.deltaY)

        self.Jason.update(dt)

        self.timeLeft -= dt;
        
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
            },
            'walls': walls_data
        }

