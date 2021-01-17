from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path

from notes import views, consumers


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', login_required(views.DashboardView.as_view()), name='dashboard'),
    path('', views.IndexView.as_view(), name='index'),
    path('<str:access_link>', views.IndexView.as_view(), name='index'),
    path('delete/<str:access_link>/', views.DeleteNoteView.as_view(), name='delete_note'),
]

websocket_urlpatterns = [
    path('<str:access_link>/<str:client>', consumers.NoteConsumer.as_asgi())
]