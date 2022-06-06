from django.urls import path
from requests import delete 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('home/', views.home, name='home'),
    path('upload/', views.upload_images, name='upload'),
    path('delete/<str:pk>', views.delete_image, name='delete'),
    path('update/<str:pk>', views.update_image, name='update'),

    path('profile/', views.profiles, name='profile'),
    path('update_profile/<str:pk>', views.update_profile, name='update-profile'),
    path('comments/<str:pk>', views.comments, name='comments')
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

