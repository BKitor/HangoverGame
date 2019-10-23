import uuid
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="quizzes")
