# Generated by Django 2.2.5 on 2019-10-08 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.CharField(default='Enter question here', max_length=100),
        ),
    ]