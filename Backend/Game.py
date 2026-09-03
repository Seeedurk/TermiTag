import eventlet
from Runner import Runner
from Tagger import Tagger
from Wall import Wall
import random
import time
import math

class Game: #TODO: 
    def __init__(self):
        self.settings = {
            "timeLimit": 10,
            "desiredRunnerLevel": 4,
            "desiredTaggerLevel": 2,
            "runnerStartX": 100,
            "runnerStartY": 300,
            "taggerStartX": 700,
            "taggerStartY": 300,
            "numberOfWalls": 5,
            "randomizeNumberOfWalls": True,
            "randomizePlayerPositions": True,
        }

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

    def apply_settings(self, settings):
        if not isinstance(settings, dict):
            return

        for key, value in settings.items():
            if key not in self.settings:
                continue

            current = self.settings[key]
            if isinstance(current, bool) and isinstance(value, bool):
                self.settings[key] = value
            elif isinstance(current, (int, float)) and isinstance(value, (int, float)):
                self.settings[key] = int(value) if isinstance(current, int) else float(value)

        self.settings["runnerStartX"] = max(0, min(int(self.settings.get("runnerStartX", 100)), 800))
        self.settings["runnerStartY"] = max(0, min(int(self.settings.get("runnerStartY", 300)), 600))
        self.settings["taggerStartX"] = max(0, min(int(self.settings.get("taggerStartX", 700)), 800))
        self.settings["taggerStartY"] = max(0, min(int(self.settings.get("taggerStartY", 300)), 600))
        self.settings["desiredRunnerLevel"] = max(1, min(int(self.settings.get("desiredRunnerLevel", 1)), 4))
        self.settings["desiredTaggerLevel"] = max(1, min(int(self.settings.get("desiredTaggerLevel", 1)), 4))
        self.settings["numberOfWalls"] = max(0, min(int(self.settings.get("numberOfWalls", 2)), 10))

        self.Mike.changeModel(self.settings["desiredRunnerLevel"])

        self.timeLeft = self.settings["timeLimit"]
        self.createWalls()

        self.gameReset()
        self.taggerScore = 0
        self.runnerScore = 0

    def _is_in_wall(self, x, y):
        for wall in self.Walls:
            if (
                wall.x <= x <= wall.x + wall.width and
                wall.y <= y <= wall.y + wall.height
            ):
                return True
        return False

    def gameReset(self):
        self.total_movement = 0.0

        self.timerReset()
        self.createWalls()

        randomize_players = self.settings.get("randomizePlayerPositions", True)

        if randomize_players:
            for _ in range(200):
                self.Mike.roundReset(randomize=True, startX=self.settings.get("runnerStartX", 100), startY=self.settings.get("runnerStartY", 300))
                if not self._is_in_wall(self.Mike.retrieveX(), self.Mike.retrieveY()):
                    break
            for _ in range(200):
                self.Jason.roundReset(randomize=True, startX=self.settings.get("taggerStartX", 700), startY=self.settings.get("taggerStartY", 300))
                if not self._is_in_wall(self.Jason.retrieveX(), self.Jason.retrieveY()):
                    break
        else:
            self.Mike.roundReset(
                randomize=False,
                startX=self.settings.get("runnerStartX", 100),
                startY=self.settings.get("runnerStartY", 300),
            )
            self.Jason.roundReset(
                randomize=False,
                startX=self.settings.get("taggerStartX", 700),
                startY=self.settings.get("taggerStartY", 300),
            )

        if self._is_in_wall(self.Mike.retrieveX(), self.Mike.retrieveY()):
            self.Mike.modifyX(100)
            self.Mike.modifyY(300)
        if self._is_in_wall(self.Jason.retrieveX(), self.Jason.retrieveY()):
            self.Jason.modifyX(700)
            self.Jason.modifyY(300)

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

    def createWalls(self, number=None):
        if number is None:
            base_count = int(self.settings.get("numberOfWalls", 2))
            if self.settings.get("randomizeNumberOfWalls", True):
                number = random.randint(0, base_count)
            else:
                number = base_count

        number = max(0, min(int(number), 10))
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
            self.Jason.taggerAIHelper(
                self.settings.get("desiredTaggerLevel", 1),
                self.Mike.retrieveX(),
                self.Mike.retrieveY(),
                self.Mike.deltaX,
                self.Mike.deltaY,
                self.Walls,
            )

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

    def _nearest_wall_distance(self, x, y):
        """
        Returns the Euclidean distance from (x, y) to the nearest wall.
        If there are no walls, returns a large value.
        """

        if not self.Walls:
            return 999.0

        nearest_distance = 999.0

        for wall in self.Walls:
            closest_x = max(wall.x, min(x, wall.x + wall.width))
            closest_y = max(wall.y, min(y, wall.y + wall.height))

            dx = closest_x - x
            dy = closest_y - y

            distance = math.hypot(dx, dy)

            if distance < nearest_distance:
                nearest_distance = distance

        return nearest_distance




    def _current_potential(self):
        rX, rY = self.Mike.retrieveX(), self.Mike.retrieveY()
        tX, tY = self.Jason.retrieveX(), self.Jason.retrieveY()
        dist = math.hypot(rX - tX, rY - tY)

        tagger_score = min(dist, 700.0) / 700.0

        margin = min(rX, 800 - rX, rY, 600 - rY)
        edge_threshold = 30                          # narrowed from 80 - only true imminent-collision zone
        edge_danger = max(0.0, (edge_threshold - margin) / edge_threshold)

        wall_margin = min(
            (math.hypot(rX - max(w.x, min(rX, w.x+w.width)), rY - max(w.y, min(rY, w.y+w.height))))
            for w in self.Walls
        ) if self.Walls else 999
        wall_threshold = 25                          # narrowed from 60
        wall_danger = max(0.0, (wall_threshold - wall_margin) / wall_threshold)

        hazard = max(edge_danger, wall_danger)

        W_TAGGER = 1.0
        W_HAZARD = 0.4                                # explicit weight, tuned down rather than 1:1

        return W_TAGGER * tagger_score - W_HAZARD * hazard


    def get_runnerReward(self):
        rX, rY = self.Mike.retrieveX(), self.Mike.retrieveY()
        tX, tY = self.Jason.retrieveX(), self.Jason.retrieveY()
        dist = math.hypot(rX - tX, rY - tY)

        # --- Terminal outcomes: unchanged ---
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

        # --- Shaping: call the same function _current_potential uses, no duplicated formula ---
        new_potential = self._current_potential()

        GAMMA = self.Mike.policy.gamma
        SHAPING_SCALE = 10.0

        shaping_reward = (GAMMA * new_potential - self.prev_potential) * SHAPING_SCALE
        self.prev_potential = new_potential

        self.reward_components["potential"] += shaping_reward

        return max(-5, min(5, shaping_reward))


    def train_step(self, action): 
        
        
        dt = 1/60

        self.Mike.modelInput(action)

        self.Jason.taggerAIHelper(
            2,
            self.Mike.retrieveX(),
            self.Mike.retrieveY(),
            self.Mike.deltaX,
            self.Mike.deltaY,
            self.Walls,
        )

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
            'walls': walls_data,
            'distance': math.hypot(self.Mike.retrieveX() - self.Jason.retrieveX(), self.Mike.retrieveY() - self.Jason.retrieveY()),
            'reward': self.get_runnerReward()
        }

