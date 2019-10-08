import uuid
from django.db import models

# Create your models here.


class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)


class Question(models.Model):
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
    #question type?
    #text?
    #
