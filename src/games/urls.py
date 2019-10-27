from django.urls import path
from . import views

urlpatterns = [
    path('api/games', views.GameList.as_view()),  # url for creating games
    path('api/players', views.PlayersListCreate.as_view()),
    path('game/<game_name>', views.GameDetailView.as_view()),  # for game details, also to add and delete players
    path('game/<game_name>/end_game', views.GameDeleteView.as_view()),
    path('game/<game_name>/next_question', views.NextQuestion.as_view())
]
