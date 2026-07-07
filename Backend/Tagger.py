import random 

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

    def basicTaggerAI(self, rX, rY):
        if(rX > self.x):
            self.accelX = 10
        else:
            self.accelX = -10

        if(rY > self.y):
            self.accelY = 10
        else:
            self.accelY = -10
    
    def roundReset(self):
        self.x = random.randint(600, 790)
        self.y = random.randint(50, 750)
        self.deltaX = 0
        self.deltaY = 0
        self.accelX = 0
        self.accelY = 0

    def update(self, dt):

        self.deltaX += self.accelX * dt
        self.deltaY += self.accelY * dt


        self.deltaX = max(-50, min(50, self.deltaX))
        self.deltaY = max(-50, min(50, self.deltaY))

        self.deltaX *= 0.98
        self.deltaY *= 0.98

        self.x += self.deltaX #figure out if * dt in neccessary here
        self.y += self.deltaY