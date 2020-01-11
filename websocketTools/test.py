import json
import websockets
import asyncio


async def test_player():

    async with websockets.client.connect("ws://192.168.1.30:8000/ws/game/g/player") as ws_player, websockets.client.connect("ws://192.168.1.30:8000/ws/game/g/host") as ws_host:

        await ws_player.send(json.dumps({"type": "game.submit_answer"}))
        print("h" + await ws_host.recv())
        print("p" + await ws_player.recv())

        await ws_host.send(json.dumps({"type": "game.lock_question"}))
        print("h" + await ws_host.recv())
        print("p" + await ws_player.recv())
        await ws_host.send(json.dumps({"type": "game.change_question"}))
        print("h" + await ws_host.recv())
        print("p" + await ws_player.recv())
        await ws_host.send(json.dumps({"type": "game.lock_question"}))
        print("h" + await ws_host.recv())
        print("p" + await ws_player.recv())
        await ws_host.send(json.dumps({"type": "game.change_question"}))
        print("h" + await ws_host.recv())
        # print("p" + await ws_player.recv()) Player doesn't receive answer
        await ws_host.send(json.dumps({"type": "game.pick_winner_loser",
                                       "payload": {"winner": "uuid", "loser": "uuid"}}))
        print("h" + await ws_host.recv())
        print("p" + await ws_player.recv())

asyncio.get_event_loop().run_until_complete(test_player())
