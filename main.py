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

    others = list(map(lambda x: Player(
        game_state["time"], x), game_state["others"]))
    powerups = list(map(lambda x: Powerup(x), game_state["powerups"]))
    if game_state["me"]["id"] == sio.get_sid():
        d = logic.choose_direction(
            game_state["time"], Player(game_state["time"], game_state["me"]), others, powerups, game_state["maze"])
        await sio.emit("update_direction", d)
    else:
        alive = False


async def main(target, botname):
    global alive

    await sio.connect(target)

    while 1:
        print("Starting game!")

        await sio.emit("game_init", botname)

        while alive:
            await asyncio.sleep(0.1)

        print("Bot got eaten, restarting in 1 second!")

        await asyncio.sleep(1)

        alive = True

    await sio.disconnect()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 main.py http://target:port BOTNAME')
        exit(1)

    target = sys.argv[1]
    botname = sys.argv[2]

    try:
        asyncio.run(main(target, botname))
    except KeyboardInterrupt:
        print("Exiting!")
