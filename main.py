#!/usr/bin/env python

import asyncio
import sys
import socketio

from bot import BotLogic
from structures import Player, Powerup


sio = socketio.AsyncClient()

logic = BotLogic()
alive = True


@sio.on('update_game')
async def update_game(game_state):
    global alive

    if not alive:
        return

    players = list(map(lambda x: Player(
        game_state["time"], x), game_state["players"]))
    powerups = list(map(lambda x: Powerup(x), game_state["powerups"]))
    if len(players) > 0 and players[-1].id == sio.get_sid():
        d = logic.choose_direction(
            game_state["time"], players[-1], players[:-1], powerups, game_state["maze"])
        await sio.emit("update_direction", d)
    else:
        alive = False


async def main(target):
    global alive

    await sio.connect(target)

    while 1:
        print("Starting game!")

        await sio.emit("game_init", "bot")

        while alive:
            await asyncio.sleep(0.1)

        print("Bot got eaten, restarting in 1 second!")

        await asyncio.sleep(1)

        alive = True

    await sio.disconnect()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 main.py http://target:port')
        exit(1)

    target = sys.argv[1]

    try:
        asyncio.run(main(target))
    except KeyboardInterrupt:
        print("Exiting!")
