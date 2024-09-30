from rest_framework import generics
from .models import BlogPost, Comment
from .serializers import BlogPostSerializer, CommentSerializer

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
    
