from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from django.contrib.auth import views as auth_views
from blog import views as blog_views



urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/<year>/<slug:title>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/new/', PostCreateView.as_view(), name='create-post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('like/', blog_views.post_like, name='like-post'),
]