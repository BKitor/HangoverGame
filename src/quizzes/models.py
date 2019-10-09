import uuid
from django.db import models

# Create your models here.


# get related questions with <Quiz>.question_set.all()
class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)


class Question(models.Model):
    default_text = "Enter question here"

    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default=default_text)
    # question type?
    # how are answers being done? are we still doing mulitple choice for some?
    # how are we linking user's answers to a question/quiz?


# Could create an answer class that has a connection to an author and to a question
