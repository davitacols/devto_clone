from rest_framework import generics
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Profile, PostInteraction, Notification
from .serializers import BlogPostSerializer, CommentSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    context = {
        'profile': profile,
        'posts': BlogPost.objects.filter(author=profile.user).order_by('-created_at')
    }
    return render(request, 'blog/profile.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    interaction, created = PostInteraction.objects.get_or_create(
        user=request.user,
        post=post,
        interaction_type='like'
    )
    
    if not created:
        # If interaction exists, delete it (unlike)
        interaction.delete()
    
    # Create notification for the post author
    if created and post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            sender=request.user,
            notification_type='like',
            post=post
        )
    
    return redirect('blog:post_detail', post_id=post.id)

@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    interaction, created = PostInteraction.objects.get_or_create(
        user=request.user,
        post=post,
        interaction_type='bookmark'
    )
    
    if not created:
        # If bookmark exists, remove it
        interaction.delete()
    
    return redirect('blog:post_detail', post_id=post.id)

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.request.query_params.get('tag_id')
        username = self.request.query_params.get('username')
        
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        if username:
            queryset = queryset.filter(author__username=username)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(BlogPost, id=post_id)
        serializer.save(author=self.request.user, post=post)

        # Create notification for the post author
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=self.request.user,
                notification_type='comment',
                post=post,
                comment=serializer.instance
            )