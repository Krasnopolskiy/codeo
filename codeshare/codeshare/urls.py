from django.contrib import admin
from django.urls import include, path
from notes import views as v


urlpatterns = [
    path('signup/', v.signup, name='signup'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('notes.urls')),
    path('', include('django.contrib.auth.urls')),
    path('userpage/', v.userPage, name='user page'),

]
