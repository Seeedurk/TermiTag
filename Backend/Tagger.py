import random 

class Tagger:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.QlilophCounter = 0
        self.deltaX = 0
        self.deltaY = 0

        self.accelX = random.randint(-25,25)
        self.accelY = random.randint(-25,25)



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
    
    def roundReset(self):
        self.x = 600
        self.y = 300
        self.deltaX = 0
        self.deltaY = 0
        self.accelX = 0
        self.accelY = 0

    def update(self, dt):

        self.modelInput()

        if(self.deltaX > 50):
            self.deltaX = 50
        if(self.deltaY > 50):
            self.deltaY = 50

        self.deltaX += self.accelX * dt
        self.deltaY += self.accelY * dt

        self.x += self.deltaX #figure out if * dt in neccessary here
        self.y += self.deltaY