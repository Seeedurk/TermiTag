import random 
import math

class Tagger:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.QlilophCounter = 0
        self.deltaX = 0
        self.deltaY = 0

        self.accelX = 0
        self.accelY = 0



        #Declare runnerPolicy
    
    def retrieveX(self):
        return self.x

    def retrieveY(self):
        return self.y

    def modifyX(self, inputX):
        self.x = inputX

    def modifyY(self, inputY):
        self.y = inputY

    def modelInput(self):
        self.accelX = random.randint(-10,10)
        self.accelY = random.randint(-10,10)
    
    
    '''
    def evaluateMove(self, accelX, accelY, rX, rY, walls, LOOK_AHEAD):
        testX = self.x
        testY = self.y
        testDX = self.deltaX
        testDY = self.deltaY

        best_distance = float("inf")

        for i in range(LOOK_AHEAD):
            testDX += accelX
            testDY += accelY

            testDX = max(-6, min(6, testDX))
            testDY = max(-6, min(6, testDY))

            testDX *= 0.98
            testDY *= 0.98

            testX += testDX
            testY += testDY

            for wall in walls:
                if (wall.x <= testX <= wall.x + wall.width and
                    wall.y <= testY <= wall.y + wall.height):
                    return -100000

            dx = rX - testX
            dy = rY - testY
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 20:
                return 100000 - i    # earlier interception scores higher than later interception

            if distance < best_distance:
                best_distance = distance

        return -best_distance
    '''

    def evaluateMove(self, accelX, accelY, rX, rY, walls, LOOK_AHEAD):
        testX = self.x
        testY = self.y
        testDX = self.deltaX
        testDY = self.deltaY

        best_distance = float("inf")

        for _ in range(LOOK_AHEAD):
            testDX += accelX
            testDY += accelY

            testDX = max(-6, min(6, testDX))
            testDY = max(-6, min(6, testDY))

            testDX *= 0.98
            testDY *= 0.98

            testX += testDX
            testY += testDY

            for wall in walls:
                if (wall.x <= testX <= wall.x + wall.width and
                    wall.y <= testY <= wall.y + wall.height):
                    return -100000

            dx = rX - testX
            dy = rY - testY
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 20:
                return 100000

            if distance < best_distance:
                best_distance = distance

        return -best_distance
    

    def lvlOneTaggerAI(self, rX, rY):
        if rX < self.x:
            self.accelX = -0.4
        elif rX > self.x:
            self.accelX = 0.4
        
        if rY < self.y:
            self.accelY = -0.4
        elif rY > self.y:
            self.accelY = 0.4


    def lvlTwoTaggerAI(self, rX, rY, walls):

        accConst = 0.4
        
        candidates = [
            (-accConst, -accConst), (-accConst, 0), (-accConst, accConst),
            (0, -accConst),                (0, accConst),
            (accConst, -accConst),  (accConst, 0),   (accConst, accConst)
        ]

        bestScore = float("-inf")
        bestAccel = (0, 0)

        for accelX, accelY in candidates:

            score = self.evaluateMove(accelX, accelY, rX, rY, walls, 30)

            if score > bestScore:
                bestScore = score
                bestAccel = (accelX, accelY)

        self.accelX = bestAccel[0]
        self.accelY = bestAccel[1]

    def predictRunnerPosition(self, rX, rY, rVX, rVY, leadTime):
        """Linear extrapolation of the runner's future position, with friction decay
        matching the runner's own physics, so the prediction stays physically plausible
        rather than assuming constant velocity forever."""
        predX, predY = rX, rY
        vx, vy = rVX, rVY
        for _ in range(leadTime):
            vx *= 0.98
            vy *= 0.98
            predX += vx
            predY += vy
        return predX, predY

    def lvlThreeTaggerAI(self, rX, rY, rVX, rVY, walls):
        accConst = 0.4
        candidates = [
            (-accConst, -accConst), (-accConst, 0), (-accConst, accConst),
            (0, -accConst),                (0, accConst),
            (accConst, -accConst),  (accConst, 0),   (accConst, accConst)
        ]

        LEAD_TIME = 10 


        predX, predY = self.predictRunnerPosition(rX, rY, rVX, rVY, LEAD_TIME)
        BLEND = 0.6 
        targetX = rX + BLEND * (predX - rX)
        targetY = rY + BLEND * (predY - rY)

        bestScore = float("-inf")
        bestAccel = (0, 0)

        for accelX, accelY in candidates:
            score = self.evaluateMove(accelX, accelY, targetX, targetY, walls, 20)
            if score > bestScore:
                bestScore = score
                bestAccel = (accelX, accelY)

        self.accelX = bestAccel[0]
        self.accelY = bestAccel[1]
        
    def taggerAIHelper(self, taggerLevel, rX, rY, rVX, rVY, walls):
        match taggerLevel:
            case 1:
                self.lvlOneTaggerAI(rX, rY)
            case 2:
                self.lvlTwoTaggerAI(rX, rY, walls)
            case 3:
                self.lvlThreeTaggerAI(rX, rY, rVX, rVY, walls)
            case 4:
                self.lvlThreeTaggerAI(rX, rY, rVX, rVY, walls)
            case _:
                raise ValueError("Invalid tagger level")

    def roundReset(self, randomize=True, startX=700, startY=300):
        if randomize:
            self.x = random.randint(700, 790)
            self.y = random.randint(50, 550)
        else:
            self.x = startX
            self.y = startY
        self.deltaX = 0
        self.deltaY = 0
        self.accelX = 0
        self.accelY = 0

    def update(self, dt):

        self.deltaX += self.accelX
        self.deltaY += self.accelY


        self.deltaX = max(-6, min(6, self.deltaX))
        self.deltaY = max(-6, min(6, self.deltaY))

        self.deltaX *= 0.98
        self.deltaY *= 0.98

        self.x += self.deltaX 
        self.y += self.deltaY