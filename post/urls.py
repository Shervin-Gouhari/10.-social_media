from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('create/', views.post_create, name='create'),
    path('detail/<slug:slug>/', views.post_detail, name='detail'),
]
