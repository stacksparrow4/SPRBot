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


class BotLogic:
    def __init__(self):
        self.dir = 0

    def choose_direction(self, time: float, me: Player, other_players: 'list[Player]', powerups: 'list[Powerup]', maze) -> float:
        # Fallback if no powerup and no players, go in circle
        self.dir += 0.1

        if not me.poweredUp:
            # If any powerups, chase after the nearest one
            shortest_dist = math.inf
            closest_power = None
            for power in powerups:
                dx = power.x - me.x
                dy = power.y - me.y
                dist = dx**2 + dy**2
                if dist < shortest_dist:
                    shortest_dist = dist
                    closest_power = power

            if not closest_power is None:
                self.dir = head_towards(me, closest_power.x, closest_power.y)

        # If any players, priorities
        for p in other_players:
            if can_eat(me, p):
                self.dir = head_towards(me, p.x, p.y)

        return self.dir
