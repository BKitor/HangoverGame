from rest_framework import generics

from games.models import Players, Game
from games.serializer import GameSerializer, PlayersSerializer

# Create your views here.


class GameListCreate(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class PlayersListCreate(generics.ListCreateAPIView):
    queryset = Players.objects.all()
    serializer_class = PlayersSerializer
