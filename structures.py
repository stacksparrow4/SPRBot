class Player:
    def __init__(self, time, data):
        self.x = data['centroid']['x']
        self.y = data['centroid']['y']
        self.id = data['id']
        self.name = data['name']
        self.team = data['team']
        self.score = data['score']
        self.poweredUp = time < data['hasPowerup']


class Powerup:
    def __init__(self, data):
        self.x = data['centroid']['x']
        self.y = data['centroid']['y']

# TODO
# class Maze:
