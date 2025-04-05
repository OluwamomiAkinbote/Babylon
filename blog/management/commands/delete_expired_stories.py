from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Story

class Command(BaseCommand):
    help = 'Delete stories that have expired (older than 7 days)'

    def handle(self, *args, **kwargs):
        # Get the current date and time
        now = timezone.now()

        # Find stories where the expiration date is before the current time
        expired_stories = Story.objects.filter(expires_at__lt=now)

        # Delete the expired stories
        count, _ = expired_stories.delete()

        if count:
            self.stdout.write(self.style.SUCCESS(f'{count} expired stories deleted successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('No expired stories found'))
