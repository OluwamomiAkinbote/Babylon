from django.core.management.base import BaseCommand
from blog.models import BlogPost
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Generate slugs for existing blog posts'

    def handle(self, *args, **kwargs):
        posts = BlogPost.objects.all()
        for post in posts:
            if not post.slug:
                post.slug = slugify(post.title)
                post.save()
                self.stdout.write(self.style.SUCCESS(f'Slug generated for post: {post.title}'))
