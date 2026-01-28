import random 

class Tagger:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.QlilophCounter = 0
        self.deltaX = random.randint(-100,100)
        self.deltaY = random.randint(-100,100)
    
    def retrieveX(self):
        return self.x

    def retrieveY(self):
        return self.y

    def modelInput(self):
        self.deltaX = random.randint(-100,100)
        self.deltaY = random.randint(-100,100)
    

    def update(self, dt):
        if(self.QlilophCounter >= 60):
           self.QlilophCounter = 0
           self.modelInput()
        self.QlilophCounter += 1
        
        self.x += self.deltaX * dt
        self.y += self.deltaY * dt