from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome),
    path('note/get/<str:note_name>', views.note_get),

    path('note/create', views.note_create),
    path('note/update', views.note_update),
    path('note/publish', views.welcome),
    path('note/delete', views.welcome),

    path('note/list', views.note_list),     # remove it
    path('author/list', views.author_list)  # remove it
]
