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

    def evaluateMove(self, accelX, accelY, rX, rY, walls):

        testX = self.x
        testY = self.y
        testDX = self.deltaX
        testDY = self.deltaY

        LOOK_AHEAD = 15

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
                if (
                    wall.x <= testX <= wall.x + wall.width and
                    wall.y <= testY <= wall.y + wall.height
                ):
                    return -100000

        dx = rX - testX
        dy = rY - testY

        distance = math.sqrt(dx * dx + dy * dy)

        return -distance

    def lvlThreeTaggerAI(self, rX, rY, walls):

        accConst = 0.25
        
        candidates = [
            (-accConst, -accConst), (-accConst, 0), (-accConst, accConst),
            (0, -accConst),                (0, accConst),
            (accConst, -accConst),  (accConst, 0),   (accConst, accConst)
        ]

        bestScore = float("-inf")
        bestAccel = (0, 0)

        for accelX, accelY in candidates:

            score = self.evaluateMove(accelX, accelY, rX, rY, walls)

            if score > bestScore:
                bestScore = score
                bestAccel = (accelX, accelY)

        self.accelX = bestAccel[0]
        self.accelY = bestAccel[1]

    def roundReset(self):
        self.x = random.randint(700, 790)
        self.y = random.randint(50, 550)
        #self.x = 700
        #self.y = 300
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

        self.x += self.deltaX #figure out if * dt in neccessary here
        self.y += self.deltaY