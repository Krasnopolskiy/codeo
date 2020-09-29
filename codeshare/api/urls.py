from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome),

    path('note/get/<str:name>', views.note_get),
    path('note/create', views.note_create),
    path('note/update', views.note_update),
    path('note/delete', views.note_delete),

    path('note/list', views.note_list)
]
