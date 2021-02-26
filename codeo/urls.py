from django.contrib.auth.views import LogoutView, LoginView
from django_registration.backends.one_step.views import RegistrationView
from django.contrib import admin
from django.urls import path

from main import views, consumers, forms


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', LoginView.as_view(
        template_name='pages/login.html',
        authentication_form=forms.LoginForm,
    ), name='login'),
    path('signup/', RegistrationView.as_view(
        template_name='pages/signup.html',
        form_class=forms.SignupForm,
        success_url='/',
        extra_context={'pagename': 'Sign up'},
    ), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name = 'activate'),
    path('', views.EditorView.as_view(), name='editor'),
    path('<str:access_link>', views.EditorView.as_view(), name='editor'),
    path('<str:access_link>/raw/', views.RawView.as_view(), name='raw'),
    path('<str:access_link>/delete/', views.DeleteView.as_view(), name='delete'),
]

websocket_urlpatterns = [
    path('<str:access_link>/<str:client>', consumers.NoteConsumer.as_asgi())
]
