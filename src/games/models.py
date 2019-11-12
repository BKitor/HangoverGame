import uuid

from django.conf import settings
from django.db import models

from quizzes.models import Quiz, Question

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
    unanswered_questions = models.ManyToManyField(Question, related_name="unanswered_questions")
    answered_questions = models.ManyToManyField(Question, related_name="answered_questions")
    current_question = None

    def init_game(self):
        for question in self.quiz.questions.all():
            self.unanswered_questions.add(question)
        self.save()

    # moves current question to answered
    # if available questions, choses next one
    # else sets current to None
    def next_question(self):
        if self.current_question:
            self.answered_questions.add(self.current_question)

        if self.unanswered_questions:
            next_q = self.unanswered_questions.first()
            self.unanswered_questions.remove(next_q)
            self.current_question = next_q
        else:
            self.current_question = None
