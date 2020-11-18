from django.urls import path, re_path
from . import views

urlpatterns = [
    path('note/create', views.api_note_create),
    # re_path(r'note/retrieve/(?P<name>\w{4,6})/$', views.api_note_retrieve)
    path('note/retrieve/<str:name>', views.api_note_retrieve)

]
