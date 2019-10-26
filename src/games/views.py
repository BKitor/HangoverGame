import json
import uuid

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from account.models import User
from games.models import Player, Game
from games.serializer import GameSerializer, PlayersSerializer

# Create your views here.


def is_valid_uuid(uuid_to_test):
    try:
        uuid.UUID(str(uuid_to_test), version=4)
        return True
    except ValueError:
        return False


class GameListCreate(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameDetailView(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = "game_name"

    # post to /game/<game_name> with player info
    # body of post has player_name, user_id(optional), and game_name in kwargs
    # returns updated game info, or 404
    def post(self, request, **kwargs):
        game = self.get_object()
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)

        user_id = body.get("user_id")
        if not user_id:
            return Response("user_id field is needed", status=status.HTTP_400_BAD_REQUEST)

        player_name = body.get("player_name")
        if not player_name:
            return Response("player_name field is needed", status=status.HTTP_400_BAD_REQUEST)

        if len(player_name) > 20:
            return Response("Player name to long, the app should have handled this case, why are you getting this response?", status=status.HTTP_400_BAD_REQUEST)

        name_exists = game.players.filter(player_name=player_name)
        if name_exists:
            return Response("That name has been taken, try a different name", status=status.HTTP_400_BAD_REQUEST)

        if is_valid_uuid(user_id):
            user = get_object_or_404(User, id=user_id)
            new_player = Player(player_name=player_name, user=user)
        else:
            new_player = Player(player_name=player_name, user=None)
        new_player.save()
        game.players.add(new_player)
        game.save()
        return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)

    # remove a player from a game
    # takes player uuid, and game as kwargs
    def delete(self, request, **kwargs):
        game = self.get_object()
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)

        user_id = body.get("user_id")
        if not user_id:
            return Response("user_id field is needed", status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_uuid(user_id):
            return Response("user_id is invalid value", status=status.HTTP_400_BAD_REQUEST)

        try:
            player = game.players.get(uuid=user_id)
        except Player.DoesNotExist:
            return Response("Provided id is not associated with this game", status=status.HTTP_404_NOT_FOUND)

        player.delete()
        return Response(f"{player.player_name} deleted", status=status.HTTP_204_NO_CONTENT)


class PlayersListCreate(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayersSerializer
