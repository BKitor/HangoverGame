from django.urls import path
from . import views

urlpatterns = [
    path('api/players', views.PlayersListCreate.as_view()),  # for game details, also to add and delete players
    path('api/players/<pk>', views.PlayerDetailView.as_view()),
    path('api/players/<pk>/update', views.PlayerUpdateView.as_view()),
    path('api/games', views.GameCreateList.as_view()),  # url for creating games get and create  players
    path('game/<game_name>', views.GameDetailView.as_view()),
    path('game/<game_name>/end_game', views.GameArchiveView.as_view()),
    path('game/<game_name>/next_question', views.GameNextQuestion.as_view()),
    path('game/<game_name>/players', views.GamePlayerList.as_view()),
    path('game/<game_name>/pick_winner_loser', views.GamePickWinnerLoser.as_view())
]
