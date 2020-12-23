from django.urls import path
from . import views

urlpatterns = [
    path('note/create', views.api_note_create),
    path('note/retrieve/<str:name>', views.api_note_retrieve),
    path('author/set', views.api_author_set)
]
