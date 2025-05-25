from django.core.management.base import BaseCommand
from blog.models import BlogPost, Category

class Command(BaseCommand):
    help = 'Move blog posts from Exclusive and its subcategories to Breaking category'

    def handle(self, *args, **kwargs):
        try:
            exclusive = Category.objects.get(name="Exclusive")
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("Category 'Exclusive' does not exist."))
            return

        subcategories = Category.objects.filter(parent=exclusive)
        all_exclusive_cats = [exclusive] + list(subcategories)

        breaking, created = Category.objects.get_or_create(name="Breaking")

        posts_to_move = BlogPost.objects.filter(category__in=all_exclusive_cats)
        count = posts_to_move.count()

        for post in posts_to_move:
            post.category = breaking
            post.save()

        self.stdout.write(self.style.SUCCESS(f"Moved {count} posts to 'Breaking' category."))
