from django.contrib import admin
from django.urls import include, path
from notes import views
from django.contrib.auth import logout


urlpatterns = [
    path('user/signup/', views.signup, name='signup'),
    path('user/login/', views.login_page, name='login'),
    path('user/home/', views.userPage, name='user page'),
    path('user/logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('notes.urls'))
]
