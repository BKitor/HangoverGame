import uuid
from django.db import models

# Create your models here.


class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __repr__(self):
        return self.name
