from django.urls import path
from . import views

urlpatterns = [
    path('api/games', views.GameCreateList.as_view()),  # url for creating games get and create  players
    path('api/players', views.PlayersListCreate.as_view()),  # for game details, also to add and delete players
    path('api/players/<pk>', views.PlayerDetailView.as_view()),
    path('api/players/<pk>/update/', views.PlayerUpdateView.as_view()),
    path('game/<game_name>', views.GameDetailView.as_view()),
    path('game/<game_name>/end_game', views.GameDeleteView.as_view()),
    path('game/<game_name>/next_question', views.NextQuestion.as_view()),
    path('game/<game_name>/players', views.PlayerList.as_view()),
]
