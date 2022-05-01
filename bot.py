import math

from structures import Player, Powerup

NUM_TEAMS = 3


def head_towards(me: Player, x: float, y: float) -> float:
    return math.atan2(y - me.y, x - me.x)


def can_eat(me: Player, them: Player) -> bool:
    if them.poweredUp:
        return False
    if me.poweredUp:
        return True
    return them.team == (me.team + 1) % NUM_TEAMS


def find_closest(me: Player, targets):
    shortest_dist = math.inf
    closest = None
    for t in targets:
        dx = t.x - me.x
        dy = t.y - me.y
        dist = dx**2 + dy**2
        if dist < shortest_dist:
            shortest_dist = dist
            closest = t
    return closest


class BotLogic:
    def __init__(self):
        self.dir = 0

    def choose_direction(self, time: float, me: Player, other_players: 'list[Player]', powerups: 'list[Powerup]', maze) -> float:
        # Fallback if no powerup and no players, go in circle
        self.dir += 0.1

        target_players = list(filter(lambda x: can_eat(me, x), other_players))
        target_powerups = [] if me.poweredUp else powerups

        targets = [*target_players, *target_powerups]

        closest = find_closest(me, targets)
        if not closest is None:
            self.dir = head_towards(me, closest.x, closest.y)

        return self.dir
