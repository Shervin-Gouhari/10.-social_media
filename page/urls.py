from django.urls import path
from . import views

app_name = "page"

urlpatterns = [
    path("", views.home, name="home"), 
    path("explore", views.explore, name="explore"), 
]
