import random

class Tagger:

    def __init__(self, x, y, deltaX, deltaY):
        self.x = x
        self.y = y
        self.deltaX = deltaX
        self.deltaY = deltaY    
    
    def retrieveX(self):
        return self.x

    def retrieveY(self):
        return self.y

    def modelInput(self):
        self.deltaX = random.randint(10,100)
        self.deltaY = random.randint(10,100)
    

    def update(self, dt):
        self.modelInput()
        self.x += self.deltaX * dt
        self.y += self.deltaY * dt
