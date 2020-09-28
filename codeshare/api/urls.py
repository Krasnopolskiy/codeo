from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome),
    path('notes/', views.notes),
    path('note/<str:note_name>', views.note),
    path('authors/', views.authors)  # remove it
]
