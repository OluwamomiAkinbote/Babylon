from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BlogPost
from .tasks import schedule_social_sharing

@receiver(post_save, sender=BlogPost)
def post_created(sender, instance, created, **kwargs):
    if created:
        schedule_social_sharing(instance.id)
