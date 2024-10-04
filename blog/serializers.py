from rest_framework import serializers
from .models import BlogPost, Comment, Tag, Profile

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['username', 'bio', 'location', 'website', 'github_username', 'twitter_username', 'profile_picture']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_username', 'created_at', 'updated_at', 'parent', 'replies']
        read_only_fields = ['author', 'post']
    
    def get_replies(self, obj):
        if obj.parent is None:  # Only get replies for parent comments
            replies = Comment.objects.filter(parent=obj)
            return CommentSerializer(replies, many=True).data
        return []

class BlogPostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_profile = ProfileSerializer(source='author.profile', read_only=True)
    tags = TagSerializer(many=True, required=False)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'cover_image', 
            'author_username', 'author_profile', 'tags', 
            'created_at', 'updated_at', 'status',
            'comments_count', 'likes_count', 'bookmarks_count'
        ]
        read_only_fields = ['author', 'slug']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.postinteraction_set.filter(interaction_type='like').count()
    
    def get_bookmarks_count(self, obj):
        return obj.postinteraction_set.filter(interaction_type='bookmark').count()
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = BlogPost.objects.create(**validated_data)
        
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            post.tags.add(tag)
        
        return post