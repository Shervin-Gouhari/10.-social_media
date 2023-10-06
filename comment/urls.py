from django.urls import path
from . import views


urlpatterns = [
    path('comment-like/', views.comment_like, name='comment_like'),
]

