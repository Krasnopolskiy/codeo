from django.contrib import admin
from django.urls import include, path
from notes import views as v
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import logout



urlpatterns = [
    #url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='user_logout'),
    path('login/', v.login_page, name = 'login'),
    path('logout/', v.logout_view, name = 'logout'),
    path('signup/', v.signup, name='signup'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('notes.urls')),
    path('', include('django.contrib.auth.urls')),
    path('userpage/', v.userPage, name='user page'),

]
