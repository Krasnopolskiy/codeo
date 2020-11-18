from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/note/update/<str:name>', consumers.NoteConsumer.as_asgi())
]
