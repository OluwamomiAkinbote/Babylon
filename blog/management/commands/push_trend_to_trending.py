from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone

from blog.models import BlogPost, BlogMedia, Category, Trend  # adjust import paths if needed

class Command(BaseCommand):
    help = 'Push all Trend entries into BlogPost under Trending category'

    def handle(self, *args, **kwargs):
        trending_category, _ = Category.objects.get_or_create(name="Trending")

        created_count = 0

        for trend in Trend.objects.all():
            slug = trend.slug or slugify(trend.title)

            if BlogPost.objects.filter(slug=slug).exists():
                self.stdout.write(self.style.WARNING(f"Skipping existing post: {slug}"))
                continue

            blog_post = BlogPost.objects.create(
                title=trend.title,
                lead=trend.content[:200],  # assuming first 200 chars as lead
                content=trend.content,
                slug=slug,
                category=trending_category,
                seo_image=trend.file if trend.is_image else None,
                date=trend.date or timezone.now()
            )

            # If there's a file (image or video), attach it via BlogMedia
            if trend.file:
                BlogMedia.objects.create(
                    blog_post=blog_post,
                    media=trend.file,
                    caption=trend.title[:300]
                )

            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"{created_count} Trend posts pushed to Trending category."))
