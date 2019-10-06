import uuid

from django.db import models

from quizzes.models import Quiz
from users.models import User

# Create your models here.


class Game(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gameName = models.CharField(max_length=50)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT, related_name="active_game_set")
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_hosting_set")

    def get_players(self):
        players = Players.objects.filter(game=self)
        return players


class Players(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="player_set")
    players = models.ManyToManyField(User, related_name="player_set")

    @classmethod
    def add_player_to_game(cls, game, user):
        player, created = cls.objects.get_or_create(game=game)
        player.players.add(user)
