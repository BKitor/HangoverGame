# Generated by Django 2.2.5 on 2019-12-23 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20191223_0311'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_joined',
            field=models.DateTimeField(auto_now=True, verbose_name='last login'),
        ),
    ]
