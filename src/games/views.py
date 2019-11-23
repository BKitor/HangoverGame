import json
import uuid

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response

from account.models import User
from games.models import Player, Game
from games.serializer import GameSerializer, PlayersSerializer
from quizzes.models import Quiz
# Create your views here.


def is_valid_uuid(uuid_to_test):
    try:
        uuid.UUID(str(uuid_to_test), version=4)
        return True
    except ValueError:
        return False


class PlayerList(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = "game_name"

    def get(self, request, **kwargs):
        game = self.get_object()
        player_arr = []
        for player in game.players.all():
            player_arr.append(player.player_name)
        return Response(player_arr, status=status.HTTP_200_OK)


class GameCreateList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    # to create a game
    # needs a host_uuid, quiz_uuid, game_name,
    def post(self, request):
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)

        host_uuid = body.get("host_uuid")
        if not host_uuid:
            return Response("host_uuid field is needed", status=status.HTTP_400_BAD_REQUEST)
        host = get_object_or_404(User, id=host_uuid)

        quiz_uuid = body.get("quiz_uuid")
        if not quiz_uuid:
            return Response("quiz_uuid field is needed", status=status.HTTP_400_BAD_REQUEST)
        quiz = get_object_or_404(Quiz, uuid=quiz_uuid)

        game_name = body.get("game_name")
        if not game_name:
            return Response("game_name field is needed", status=status.HTTP_400_BAD_REQUEST)
        name_taken = Game.objects.filter(game_name=game_name)
        if name_taken:
            return Response("Name is taken, choose a new name", status=status.HTTP_400_BAD_REQUEST)

        new_game = Game(game_name=game_name, host=host, quiz=quiz)
        new_game.save()
        new_game.init_game()
        return Response(GameSerializer(new_game).data, status=status.HTTP_201_CREATED)


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
        return Response(PlayersSerializer(new_player).data, status=status.HTTP_201_CREATED)

    # remove a player from a game
    # takes player uuid, and game as kwargs
    def delete(self, request, **kwargs):
        game = self.get_object()
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)

        player_id = body.get("player_id")
        if not player_id:
            return Response("player_id field is needed", status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_uuid(player_id):
            return Response("player_id is invalid value", status=status.HTTP_400_BAD_REQUEST)

        try:
            player = game.players.get(uuid=player_id)
        except Player.DoesNotExist:
            return Response("Provided id is not associated with this game", status=status.HTTP_404_NOT_FOUND)

        player.delete()
        return Response(f"{player.player_name} deleted", status=status.HTTP_204_NO_CONTENT)


class GameDeleteView(generics.DestroyAPIView):
    lookup_field = "game_name"
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class PlayersListCreate(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayersSerializer


class PlayerDetailView(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayersSerializer

    def get(self, request, pk):
        try:
            player = Player.objects.get(uuid=pk)
        except (ValidationError, User.DoesNotExist):
            return Response("Invalid user ID", status=status.HTTP_400_BAD_REQUEST)

        serializer = PlayersSerializer(player)
        return Response(serializer.data)


class PlayerUpdateView(generics.UpdateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayersSerializer

    def put(self, request, pk):
        try:
            player = Player.objects.get(uuid=pk)
        except (ValidationError, Player.DoesNotExist):
            return Response("Invalid user ID", status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(request.body)
        new_name = body.get("player_name")

        if not new_name:
            return Response("player_name is a required field", status=status.HTTP_400_BAD_REQUEST)

        player.player_name = new_name
        player.save()

        serializer = PlayersSerializer(player)
        return Response(serializer.data)


class NextQuestion(generics.GenericAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = "game_name"

    # Update the game to the next question
    # takes game name in kwargs and user_id
    # only host can update, so check user_id
    def put(self, request, **kwargs):
        game = self.get_object()
        body = request.body

        if not body.decode('UTF-8'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(body)

        user_id = body.get("user_id")
        if not user_id:
            return Response("user_id field is needed", status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_uuid(user_id):
            return Response("Malformed user_id", status=status.HTTP_400_BAD_REQUEST)

        if user_id != game.host.id:
            return Response("Not authorize to update game", status=status.HTTP_403_FORBIDDEN)

        game.next_question()
        return Response(GameSerializer(game), status=status.HTTP_202_ACCEPTED)
