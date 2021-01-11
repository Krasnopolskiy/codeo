from django.contrib import admin
from django.urls import include, path
from notes import views
from django.contrib.auth import logout


urlpatterns = [
    path('api/', include('api.urls')),
    path('', include('notes.urls'))
]
