from django.urls import path
from . import views

urlpatterns = [
    path('api/games/games', views.GameListCreate.as_view()),
    path('api/games/players', views.PlayersListCreate.as_view()),
    path('game/<game_name>', views.GameDetailView.as_view())
]
