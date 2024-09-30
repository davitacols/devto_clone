from django.urls import path
from .views import BlogPostListCreate, BlogPostDetail, CommentListCreate

urlpatterns = [
    path('posts/', BlogPostListCreate.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', BlogPostDetail.as_view(), name='post-detail'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
]
