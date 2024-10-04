from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/bookmark/', views.bookmark_post, name='bookmark_post'),
    path('posts/', views.BlogPostListCreate.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', views.BlogPostDetail.as_view(), name='post_detail'),
    path('posts/<int:post_id>/comments/', views.CommentListCreate.as_view(), name='comment_list_create'),
]