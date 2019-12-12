from games.models import Game
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class GameJsonWebsocketConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_name = self.scope['url_route']['kwargs']['game_name']

    # gaurentees the subcalles have certain methods at 'compile time'
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        assert hasattr(cls, 'game_submit_answer')
        assert hasattr(cls, 'game_lock_question')
        assert hasattr(cls, 'game_change_question')
        assert hasattr(cls, 'game_question_changed')
        assert hasattr(cls, 'game_pick_winner_loser')
        assert hasattr(cls, 'game_player_joined')
        assert hasattr(cls, 'game_player_leaving')
        assert hasattr(cls, 'game_end_game')
        assert hasattr(cls, 'game_start_game')

    def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game_name']
        self.game_group_name = f"game_{self.game_name}"

        async_to_sync(self.channel_layer.group_add)(self.game_group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.game_group_name, self.channel_name)

    # recieves a message and sends it to the group_channel_layer
    def receive_json(self, content):

        # Receives a json object, commands include: next_questing, lock_question, chose_winner_loser
        if 'type' not in content:
            self.send_json(content={"error": "json field 'type' is required"})
            return

        if content['type'] not in self.possible_commands:
            # throw error
            self.send_json(content={"error": f"{content['type']} is not a viable type"})
            return

        if 'payload' not in content:
            content['payload'] = {}

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {
                'type': content['type'],
                'payload': content['payload']
            }
        )


class HostConsumer(GameJsonWebsocketConsumer):
    # listens to submit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.possible_commands = ['game.change_question',
                                  'game.lock_question',
                                  'game.pick_winner_loser',
                                  'game.start_game']
        self.game_model = Game.objects.get(game_name=self.game_name)
        self.game_model.question_locked = False
        self.game_model.game_over = False

    def game_lock_question(self, event):
        self.game_model.question_locked = not self.game_model.question_locked
        self.send_json({'type': 'sucsess', 'payload': 'question locked'})

    def game_change_question(self, event):
        if not self.game_model.question_locked:
            self.send_json({'type': 'error', 'payload': 'Quesiton not locked when tring to change question'})
            return
        if self.game_model.game_over:
            self.send_json({'type': 'error', 'payload': "Game is over, can't change question"})

        self.game_model.next_question()
        if self.game_model.current_question is None:
            self.game_model.game_over = True

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {
                'type': 'game.question_changed',
                'payload': {'question_uuid': str(self.game_model.current_question.uuid) if self.game_model.current_question else None}
            }
        )
        print(f"{self}\t{event}")
        self.send_json({'type': 'sucsess', 'payload': 'question changed'})

    def game_pick_winner_loser(self, event):
        #  find some way to track the winner/loser
        self.send_json({'type': 'sucsess', 'payload': 'winner/loser picked'})

    def game_submit_answer(self, event):
        # update frontend
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_question_changed(self, event):
        pass

    def game_end_game(self, event):
        # archive the game
        self.send_json({'type': 'sucsess', 'payload': 'game ended'})

    def game_player_joined(self, event):
        # update the frontend
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_player_leaving(self, event):
        # update the frontend
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_start_game(self, event):
        print(f"{self}\t{event}")
        self.send_json(event)


class PlayerConsumer(GameJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.possible_commands = ['game.submit_answer', 'game.player_joined', 'game.player_leaving']

    def game_submit_answer(self, event):
        # update frontend
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_lock_question(self, event):
        # update frontend
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_question_changed(self, event):
        # update frontned
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_pick_winner_loser(self, event):
        # update frontend, and notify winner/loser
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_player_joined(self, event):
        # update fronend
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_player_leaving(self, event):
        # update frontend
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_start_game(self, event):
        # update frontend
        print(f"{self}\t{event}")
        self.send_json(event)

    def game_end_game(self, event):
        # update frontend
        print(f"{self}\t{event}")
        self.send_json(event)

    # needs to run after host as updated the question
    def game_change_question(slef, event):
        pass
