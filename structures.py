class Player:
    def __init__(self, time, data):
        self.x = data['x']
        self.y = data['y']
        self.id = data['id']
        self.name = data['name']
        self.team = data['team']
        self.score = data['score']
        self.poweredUp = time < data['hasPowerup']


class Powerup:
    def __init__(self, data):
        self.x = data['x']
        self.y = data['y']

# TODO
# class Maze:
