import uuid
from django.db import models
from django.contrib import auth


# Create your models here.

class User(auth.models.AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_joined = models.DateTimeField(verbose_name="last login", auto_now=True)

    def getQuizzes(self):
        return self.quiz_set.all()
