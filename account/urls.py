from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.registration, name='registration'),
    path('registration/verification_code/', views.verification_code, name='verification_code'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
