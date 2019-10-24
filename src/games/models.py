import uuid

from django.conf import settings
from django.db import models

from quizzes.models import Quiz

# Create your models here.


class Game(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game_name = models.CharField(max_length=50, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT, related_name="active_game_set")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_hosting_set")

    def get_players(self):
        players = Players.objects.filter(game=self)
        return players


class Players(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="player_set")
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="player_set")

    @classmethod
    def add_player_to_game(cls, game, user):
        player, created = cls.objects.get_or_create(game=game)
        player.players.add(user)
