from django.contrib.auth import views as django_views
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', django_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('registration/', views.registration, name='registration'),
    path('registration/verification_code/', views.verification_code, name='verification_code'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('chaining/', include('smart_selects.urls')),
    path('follow/', views.follow, name='follow'),
    path('search/', views.search, name='search'),
    path('following/', views.following, name='following'),
]
