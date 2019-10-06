import uuid

from django.db import models

# Create your models here.


class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    screen_name = models.CharField(max_length=100)
    # email
    # Quizzes[]?

    def __repr__(self):
        return self.screen_name
