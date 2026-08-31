import os
import random 
from Policy.DQNPolicy import DQNPolicy
from Models.model import LinearQNet


class Runner:

    def __init__(self, x, y, is_training=False):
        self.x = x
        self.y = y
        self.QlilophCounter = 0
        self.deltaX = 0
        self.deltaY = 0

        self.accelX = 0
        self.accelY = 0
        self.level = 3

        state_size=23
        action_size=4
        hidden_size=128
        
        model = LinearQNet(state_size, hidden_size, action_size)
        self.policy = DQNPolicy(model, state_size, action_size)

        self.loadModelForMode(is_training)

    def loadModelForMode(self, is_training=False):
        os.makedirs("./model", exist_ok=True)

        if is_training:
            training_path = os.path.join("./model", "model.pth")
            meta_path = os.path.join("./model", "meta.pth")

            self.policy.n_games = 0

            if os.path.exists(training_path):
                self.policy.load("model.pth", meta_path=meta_path)
            else:
                self.policy.model.save("model.pth")
                self.policy.load("model.pth", meta_path=meta_path)

            self.policy.n_games = 0
            self.policy.save("model.pth", meta_path=meta_path)
            print("Training mode: using model.pth only")
            return

        self.changeModel(self.level)

    def changeModel(self, desiredLevel):
        try:
            match desiredLevel:
                case 1:
                    self.policy.load("UntrainedModel.pth", meta_path="./model/UntrainedMeta.pth")
                case 2:
                    self.policy.load("2500Model.pth", meta_path="./model/2500ModelMeta.pth")
                case 3:
                    self.policy.load("5kModel.pth", meta_path="./model/5kModelMeta.pth")
        
        except FileNotFoundError:
            print("Model or Meta file not found. Change not applied.")
        
    
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
            self.accelY = -0.4
        elif action == 1:
            self.accelX = 0
            self.accelY = +0.4
        elif action == 2:
            self.accelX = -0.4
            self.accelY = 0
        elif action == 3:
            self.accelX = +0.4
            self.accelY = 0


    def roundReset(self, randomize=True, startX=100, startY=300):
        if randomize:
            self.x = random.randint(50, 300)
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
        #Velocity damping for friction
        self.deltaX *= 0.98
        self.deltaY *= 0.98

        self.x += self.deltaX
        self.y += self.deltaY