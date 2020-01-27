from random import random

from django.test import TestCase, Client
from account.models import User
from games.models import Player
from quizzes.models import Quiz, Question
from games.models import Game
# Create your tests here.


class PlayerTestCase(TestCase):

    def assert_equal_user_player(self, player_dict, player_obj):
        self.assertEqual(player_dict['player_name'], player_obj.player_name)
        self.assertEqual(player_dict['user'], str(player_obj.user.id))

    def assert_equal_anon_player(self, player_dict, player_obj):
        self.assertEqual(player_dict['player_name'], player_obj.player_name)
        self.assertEqual(player_dict['user'], str(player_obj.user.id))

    @property
    def sample_user_player_dict(self):
        user, _ = User.objects.get_or_create(username="test_user")

        return {
            "player_name": "Test_player",
            "user": str(user.id)
        }

    @property
    def sample_anon_player_dict(self):
        return {
            "player_name": "Test_player",
            "user": "anything but a proper id"
        }

    def test_user_player_create(self):
        c = Client()
        req_url = "/api/players"
        req_body = self.sample_user_player_dict

        res = c.post(req_url, req_body, content_type="application/json")

        new_player = Player.objects.get(uuid=res.json()['uuid'])

        self.assert_equal_user_player(req_body, new_player)


class GameTestCase(TestCase):
    # def tearDown(self):
    #     # print(self.sample_quiz.questions.all())
    #     # print(Quiz.objects.get(name="setUpQuiz").questions.all())

    @property
    def sample_player(self):
        p = Player.objects.create(player_name=f"test_player-{random()}")
        p.save()
        return p

    @property
    def sample_game(self):
        game, _ = Game.objects.get_or_create(
            host=self.sample_user, quiz=self.sample_quiz, game_name="SampleGame")
        return game

    @property
    def sample_user(self):
        user, _ = User.objects.get_or_create(username=f"test_username-{random()}")
        return user

    @property
    def sample_quiz(self):
        user = self.sample_user
        question = Question.objects.create(prompt="test_question_prompt")
        quiz, _ = Quiz.objects.get_or_create(name="test_quiz", author=user)
        quiz.questions.set([question])
        return quiz

    def test_game_create(self):
        c = Client()
        req_url = "/api/games"
        test_host = self.sample_user
        test_quiz = self.sample_quiz
        req_body = {
            "host_uuid": str(test_host.id),
            "quiz_uuid": str(test_quiz.uuid),
            "game_name": "test_game"
        }

        res = c.post(req_url, req_body, content_type="application/json")

        new_game = Game.objects.get(uuid=res.json()['uuid'])
        self.assertEqual(new_game.game_name, req_body['game_name'])
        self.assertEqual(str(new_game.host.id), req_body['host_uuid'])

    def test_game_archive(self):
        c = Client()
        test_game = self.sample_game
        req_url = f"/game/{test_game.game_name}/end_game"

        c.delete(req_url)

        g = Game.objects.get(uuid=test_game.uuid)
        self.assertEqual(g.archived, True)

    def test_change_player_name(self):
        c = Client()
        test_game = self.sample_game
        old_player = {
            "player_name": "Test_player",
            "user_id": " "
        }

        res = c.post(f"/game/{test_game.game_name}", old_player, content_type="application/json")
        old_player = Player.objects.get(uuid=res.json()['uuid'])

        update_player = {
            "player_name": "updated username"
        }

        res = c.put(f"/api/players/{old_player.uuid}/update", update_player, content_type="application/json")
        new_player = Player.objects.get(uuid=res.json()['uuid'])

        self.assertNotEqual(old_player.player_name, new_player.player_name)
        self.assertEquals(new_player.player_name, "updated username")

    def test_player_list(self):
        c = Client()
        sample_game = self.sample_game

        test_player_names = [
            'test_name_1',
            'test_name_2',
            'test_name_3'
        ]

        req_body = {
            'user_id': 'anon',
            'player_name': None,
        }
        for i in range(3):
            req_body['player_name'] = test_player_names[i]
            res = c.post(f'/game/{sample_game.game_name}', req_body, 'application/json')

        res = c.get(f'/game/{sample_game.game_name}/players')
        for name in res.json():
            self.assertIn(name, test_player_names)

    def test_pick_winner_loser(self):
        c = Client()
        sample_game = self.sample_game
        sample_game.init_game()
        p1 = self.sample_player
        p2 = self.sample_player
        sample_game.players.set([p1, p2])
        sample_game.next_question()
        sample_game.refresh_from_db()

        req_url = f'/game/{sample_game.game_name}/pick_winner_loser'
        req_body = {
            'winner': str(p1.uuid),
            'loser': str(p2.uuid),
            'question': str(sample_game.current_question.uuid)
        }

        res = c.post(req_url, req_body, content_type='application/json')

        self.assertEqual(res.json()['winner'], str(p1.uuid))
        self.assertEqual(res.json()['loser'], str(p2.uuid))
