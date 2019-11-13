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

    def setUp(self):
        q1 = Question.objects.create(prompt="Question 1")
        q2 = Question.objects.create(prompt="Question 2")
        q3 = Question.objects.create(prompt="Question 3")

        Q1 = Quiz.objects.create(author=self.sample_user, name="setUpQuiz")

        Q1.questions.add(q1)
        Q1.questions.add(q2)
        Q1.questions.add(q3)

    # def tearDown(self):
    #     # print(self.sample_quiz.questions.all())
    #     # print(Quiz.objects.get(name="setUpQuiz").questions.all())

    @property
    def sample_game(self):
        game, _ = Game.objects.get_or_create(
            host=self.sample_user, quiz=self.sample_quiz, game_name="SampleGame")
        return game

    @property
    def sample_user(self):
        user, _ = User.objects.get_or_create(username="test_username")
        return user

    @property
    def sample_quiz(self):
        user = self.sample_user
        quiz, _ = Quiz.objects.get_or_create(name="test_quiz", author=user)
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

    def test_game_delete(self):
        c = Client()
        test_game = self.sample_game
        req_url = f"/game/{test_game.game_name}/end_game"

        c.delete(req_url)

        try:
            Game.objects.get(uuid=test_game.uuid)
            self.assertEqual(1, 0, "game was not deleted")
        except Game.DoesNotExist:
            self.assertEqual(1, 1, "game was deleted")

    def test_change_player_name(self):
        c = Client()
        test_game = self.sample_game
        old_player = {
            "player_name": "Test_player",
            "user_id": " "
        }

        res = c.post(f"/game/{test_game.game_name}", old_player, content_type="application/json")
        old_player = Player.objects.get(uuid=res.json()['players'][0])

        update_player = {
            "player_name": "updated username"
        }

        res = c.put(f"/api/players/{old_player.uuid}/update/", update_player, content_type="application/json")
        new_player = Player.objects.get(uuid=res.json()['uuid'])

        self.assertNotEqual(old_player.player_name, new_player.player_name)
        self.assertEquals(new_player.player_name, "updated username")
