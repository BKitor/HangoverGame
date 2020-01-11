from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<game_name>\w+)/player$', consumers.PlayerConsumer),
    re_path(r'ws/game/(?P<game_name>\w+)/host$', consumers.HostConsumer),
]
