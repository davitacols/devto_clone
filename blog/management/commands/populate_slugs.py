from django.core.management.base import BaseCommand
from blog.models import BlogPost
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates empty slugs for all blog posts'

    def handle(self, *args, **kwargs):
        posts = BlogPost.objects.filter(slug='')
        for post in posts:
            original_slug = slugify(post.title)
            slug = original_slug
            counter = 1
            
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            post.slug = slug
            post.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully added slug "{slug}" to post "{post.title}"')
            )