from rest_framework import serializers
from games.models import Game, Player, AnsweredQuestion


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class AnsweredQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnsweredQuestion
        fields = '__all__'
