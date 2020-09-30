from django.urls import path, re_path
from . import views

urlpatterns = [
    path('welcome/', views.welcome),
    path('note/create', views.note_create),
    re_path(r'note/retrieve/(?P<name>\w{4})/$', views.note_retrieve),
    path('note/update', views.note_update),
    path('note/delete', views.note_delete)
]
