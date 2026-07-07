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

        state_size=14
        action_size=4
        hidden_size=256
        
        model = LinearQNet(state_size, hidden_size, action_size)
        self.policy = DQNPolicy(model, state_size, action_size)

        try:
            self.policy.load("model.pth")
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
            self.accelY = -20
        elif action == 1:
            self.accelX = 0
            self.accelY = +20
        elif action == 2:
            self.accelX = -20
            self.accelY = 0
        elif action == 3:
            self.accelX = +20
            self.accelY = 0

    def roundReset(self):
        self.x = 100
        self.y = 300
        self.deltaX = 0
        self.deltaY = 0
        self.accelX = 0
        self.accelY = 0

    def update(self, dt):



        self.deltaX += self.accelX * dt
        self.deltaY += self.accelY * dt

        self.deltaX = max(-50, min(50, self.deltaX))
        self.deltaY = max(-50, min(50, self.deltaY))
        #Velocity damping for friction
        self.deltaX *= 0.98
        self.deltaY *= 0.98

        self.x += self.deltaX
        self.y += self.deltaY