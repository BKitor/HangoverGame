import uuid
from django.db import models
from django.conf import settings


# Create your models here.

# to get all associated quizzes - <question>.quiz_set.all()


class Question(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.CharField(max_length=100, editable=False)
    # question type?


class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
