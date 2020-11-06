from django.urls import path, re_path
from . import views, consumer

urlpatterns = [
    path('note/create', views.api_note_create),
    re_path(r'note/retrieve/(?P<name>\w{4,6})/$', views.api_note_retrieve)
]

websocket_urlpatterns = [
    path('ws/note/update', consumer.NoteConsumer.as_asgi())
]
