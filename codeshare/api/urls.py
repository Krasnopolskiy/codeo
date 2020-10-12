from django.urls import path, re_path
from . import views

urlpatterns = [
    path('welcome/', views.api_welcome),
    path('note/create', views.api_note_create),
    re_path(r'note/retrieve/(?P<name>\w{4})/$', views.api_note_retrieve),
    path('note/update', views.api_note_update),
    path('note/delete', views.api_note_delete),
    path('note/invite_collaborator', views.api_note_invite_collaborator)
]
