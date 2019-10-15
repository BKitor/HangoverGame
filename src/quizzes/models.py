import uuid
from django.db import models

# Create your models here.


class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    questions = models.ManyToManyField("Question")


# to get all associated quizzes - <question>.quiz_set.all()
class Question(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.CharField(max_length=100)
    # question type?
