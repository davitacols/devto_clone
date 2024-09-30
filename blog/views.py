from rest_framework import generics
from .models import BlogPost, Comment, Profile, PostInteraction, Notification
from .serializers import BlogPostSerializer, CommentSerializer
from django.shortcuts import render, get_object_or_404, redirect

def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'blog/profile.html', {'profile': profile})

def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    interaction, created = PostInteraction.objects.get_or_create(user=request.user, post=post)
    if created or not interaction.liked:
        interaction.liked = not interaction.liked
        interaction.save()
    return redirect('blog:post_detail', post_id=post.id)


class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.request.query_params.get('tag_id')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        return queryset


class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
