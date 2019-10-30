import uuid
from django.db import models
from django.conf import settings


# Create your models here.

class Question(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.CharField(max_length=100)
    # question type?

    def getQuizzes(self):
        return self.quiz_set.all()


class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
