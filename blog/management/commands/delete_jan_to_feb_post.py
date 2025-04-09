from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import BlogPost
from datetime import datetime

class Command(BaseCommand):
    help = 'Delete blog posts from January to February of the current year'

    def handle(self, *args, **kwargs):
        current_year = timezone.now().year
        start_date = datetime(current_year, 1, 1, tzinfo=timezone.get_current_timezone())
        end_date = datetime(current_year, 3, 1, tzinfo=timezone.get_current_timezone())

        posts_to_delete = BlogPost.objects.filter(date__gte=start_date, date__lt=end_date)
        count = posts_to_delete.count()

        if count > 0:
            posts_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} blog post(s) from Jan to Feb {current_year}'))
        else:
            self.stdout.write(self.style.WARNING(f'No blog posts found between Jan and Feb {current_year}'))
