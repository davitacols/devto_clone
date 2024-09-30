from django.urls import path
from .views import BlogPostListCreate, BlogPostDetail, CommentListCreate, profile_view, like_post

urlpatterns = [
    path('posts/', BlogPostListCreate.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', BlogPostDetail.as_view(), name='post-detail'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('profile/<str:username>/', profile_view, name='profile_view'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
]
