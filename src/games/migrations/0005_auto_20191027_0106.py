# Generated by Django 2.2.5 on 2019-10-27 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_auto_20191026_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='answered_questions',
            field=models.ManyToManyField(db_constraint=False, related_name='answered_questions', to='quizzes.Question'),
        ),
        migrations.AlterField(
            model_name='game',
            name='unanswered_questions',
            field=models.ManyToManyField(db_constraint=False, related_name='unanswered_questions', to='quizzes.Question'),
        ),
    ]
