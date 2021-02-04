from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path

from main import views, consumers


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('source/<str:access_link>/', views.DownloadView.as_view(), name='download'),
    path('delete/<int:id>/', views.DeleteView.as_view(), name='delete'),
    path('', views.EditorView.as_view(), name='editor'),
    path('<str:access_link>', views.EditorView.as_view(), name='editor'),
]

websocket_urlpatterns = [
    path('<str:access_link>/<str:client>', consumers.NoteConsumer.as_asgi())
]
