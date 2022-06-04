from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gram_app.urls')),
    path('accounts/', include('gram_app.urls')),
    path('auth/', include('allauth.urls')),
]
