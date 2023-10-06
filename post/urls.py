from django.urls import path, include
from . import views

app_name = 'post'

urlpatterns = [
    path('create/', views.post_create, name='create'),
    path('delete/<slug:slug>/', views.post_delete, name='delete'),
    path('edit/<slug:slug>/', views.post_edit, name='edit'),
    path('detail/<slug:slug>/', views.post_detail, name='detail'),
    path('detail/<slug:slug>/API', views.PostDetailAPI.as_view(), name='detail_API'),
    path('post-like/', views.post_like, name='post_like'),
    path('post-save/', views.post_save, name='post_save'),
    path('', include('comment.urls')),
]

