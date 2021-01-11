from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.IndexView.as_view(), name='index'),
    path('<str:name>', views.IndexView.as_view(), name='index')
]
