from django.db import models

# Create your models here.


class User(models.Model):
    uuid = models.CharField(max_length=32)
    screen_name = models.CharField(max_length=100)
    # email
    # Quizes[]?