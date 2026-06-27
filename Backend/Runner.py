import random 
from Policy.DQNPolicy import DQNPolicy
from Models.model import LinearQNet


class Runner:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.QlilophCounter = 0
        self.deltaX = 0
        self.deltaY = 0

        self.accelX = 0
        self.accelY = 0

        state_size=10
        action_size=4
        hidden_size=256
        
        model = LinearQNet(state_size, hidden_size, action_size)
        self.policy = DQNPolicy(model, state_size, action_size)

        try:
            self.policy.load("latest.pth")
        except FileNotFoundError:
            print("Creating new Model File")


        #Declare runnerPolicy
    
    def retrieveX(self):
        return self.x

    def retrieveY(self):
        return self.y

    def modifyX(self, inputX):
        self.x = inputX

    def modifyY(self, inputY):
        self.y = inputY


    def modelInput(self, action):

        if(action == 0):
            self.accelX = 0
            self.accelY = -10
        elif action == 1:
            self.accelX = 0
            self.accelY = +10
        elif action == 2:
            self.accelX = -10
            self.accelY = 0
        elif action == 3:
            self.accelX = +10
            self.accelY = 0

    def roundReset(self):
        self.x = 200
        self.y = 300
        self.deltaX = 0
        self.deltaY = 0
        self.accelX = 0
        self.accelY = 0

    def update(self, dt):

        if(self.deltaX > 50):
            self.deltaX = 50
        if(self.deltaY > 50):
            self.deltaY = 50

        self.deltaX += self.accelX * dt
        self.deltaY += self.accelY * dt

        self.x += self.deltaX #figure out if * dt in neccessary here
        self.y += self.deltaY