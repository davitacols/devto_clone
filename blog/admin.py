from django.contrib import admin
from .models import BlogPost, Comment, Profile, Tag, PostInteraction, Notification

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(PostInteraction)
admin.site.register(Notification)
