
class Runner:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def retrieveX(self):
        return self.x

    def retrieveY(self):
        return self.y

    def update(self, deltaX, deltaY, dt):
        self.x += deltaX * dt
        self.y += deltaY * dt
