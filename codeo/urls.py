from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from main import consumers, forms, views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.ExtendedLoginView.as_view(
        template_name='registration/login.html',
        authentication_form=forms.LoginForm,
        extra_context={'pagename': 'Log in'},
    ), name='login'),
    path('signup/', views.ExtendedRegistrationView.as_view(
        template_name='registration/signup.html',
        form_class=forms.SignupForm,
        success_url='/',
        extra_context={'pagename': 'Sign up'},
    ), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('', views.EditorView.as_view(), name='editor'),
    path('<str:access_link>', views.EditorView.as_view(), name='editor'),
    path('<str:access_link>/raw/', views.RawView.as_view(), name='raw'),
    path('<str:access_link>/delete/', views.DeleteView.as_view(), name='delete'),
]

websocket_urlpatterns = [
    path('<str:access_link>/<str:client>', consumers.NoteConsumer.as_asgi())
]
