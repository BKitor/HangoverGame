#!/home/bkitor/Documents/Projects/HangoverGame/.venv/bin/python

import json
import websockets
import requests
import asyncio

game_name = "G"
server_addr = "localhost:8000"

p1_uuid = requests.post(f"http://{server_addr}/game/{game_name}", json={
    'player_name': 'p1',
    'user_id': 'anon'
}).json()['uuid']

p2_uuid = requests.post(f"http://{server_addr}/game/{game_name}", json={
    'player_name': 'p2',
    'user_id': 'anon'
}).json()['uuid']

p3_uuid = requests.post(f"http://{server_addr}/game/{game_name}", json={
    'player_name': 'p3',
    'user_id': 'anon'
}).json()['uuid']

p4_uuid = requests.post(f"http://{server_addr}/game/{game_name}", json={
    'player_name': 'p4',
    'user_id': 'anon'
}).json()['uuid']


async def test_player():

    async with websockets.client.connect("ws://localhost:8000/ws/game/G/player") as ws_player1, websockets.client.connect("ws://localhost:8000/ws/game/G/player") as ws_player2, websockets.client.connect("ws://localhost:8000/ws/game/G/player") as ws_player3, websockets.client.connect("ws://localhost:8000/ws/game/G/player") as ws_player4:
        # p1_join
        await ws_player1.send(json.dumps({"type": "game.player_joined", "payload": {"player_name": "test_p_1"}}))
        print(await ws_player1.recv())
        await ws_player2.recv()
        await ws_player3.recv()
        await ws_player4.recv()

        # p2_join
        await ws_player2.send(json.dumps({"type": "game.player_joined", "payload": {"player_name": "test_p_2"}}))
        print(await ws_player1.recv())
        await ws_player2.recv()
        await ws_player3.recv()
        await ws_player4.recv()

        # p3_join
        await ws_player2.send(json.dumps({"type": "game.player_joined", "payload": {"player_name": "test_p_3"}}))
        print(await ws_player1.recv())
        await ws_player2.recv()
        await ws_player3.recv()
        await ws_player4.recv()
        # p4_join
        await ws_player2.send(json.dumps({"type": "game.player_joined", "payload": {"player_name": "test_p_4"}}))
        print(await ws_player1.recv())
        await ws_player2.recv()
        await ws_player3.recv()
        await ws_player4.recv()

        # start_game
        print(await ws_player1.recv())
        await ws_player2.recv()
        await ws_player3.recv()
        await ws_player4.recv()

        for i in range(0, 3):

            # p1 send response
            await ws_player1.send(json.dumps({"type": "game.submit_answer", "payload": {"answer_text": "test_ans1", "player_uuid": f"{p1_uuid}"}}))
            print(await ws_player1.recv())
            await ws_player2.recv()
            await ws_player3.recv()
            await ws_player4.recv()

            # p2 send response
            await ws_player2.send(json.dumps({"type": "game.submit_answer", "payload": {"answer_text": "test_ans2", "player_uuid": f"{p2_uuid}"}}))
            print(await ws_player1.recv())
            await ws_player2.recv()
            await ws_player3.recv()
            await ws_player4.recv()

            # p2 send response
            await ws_player3.send(json.dumps({"type": "game.submit_answer", "payload": {"answer_text": "test_ans3", "player_uuid": f"{p3_uuid}"}}))
            print(await ws_player1.recv())
            await ws_player2.recv()
            await ws_player3.recv()
            await ws_player4.recv()

            # p2 send response
            await ws_player4.send(json.dumps({"type": "game.submit_answer", "payload": {"answer_text": "test_ans4", "player_uuid": f"{p4_uuid}"}}))
            print(await ws_player1.recv())
            await ws_player2.recv()
            await ws_player3.recv()
            await ws_player4.recv()

            # lock question
            print(await ws_player1.recv())
            await ws_player2.recv()
            await ws_player3.recv()
            await ws_player4.recv()

            recvd_message = {"type": "not a thing"}
            while(not (recvd_message["type"] == "game.pick_winner_loser")):
                # pick winner loser
                recvd_message = json.loads(await ws_player1.recv())
                await ws_player2.recv()
                await ws_player3.recv()
                await ws_player4.recv()

                print(recvd_message)

            # changed question
            print(await ws_player1.recv())
            await ws_player2.recv()
            await ws_player3.recv()
            await ws_player4.recv()


asyncio.get_event_loop().run_until_complete(test_player())
