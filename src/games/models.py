import uuid

from django.conf import settings
from django.db import models

from quizzes.models import Quiz

# Create your models here.


class Player(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player_name = models.CharField(editable=True, max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)


class Game(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game_name = models.CharField(max_length=50, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT, related_name="active_game_set")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_hosting_set")
    players = models.ManyToManyField(Player)
