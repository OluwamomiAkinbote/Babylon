import os
import json
from celery import shared_task
import tweepy
import facebook
from twilio.rest import Client
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import timedelta
from .models import BlogPost

@shared_task
def share_to_twitter(post_id):
    post = BlogPost.objects.get(id=post_id)
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweet = f"{post.title} - {post.get_absolute_url()}"
    api.update_status(tweet)
    post.is_shared_twitter = True
    post.save()

@shared_task
def share_to_facebook(post_id):
    post = BlogPost.objects.get(id=post_id)
    page_access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    graph = facebook.GraphAPI(page_access_token)

    post_url = post.get_absolute_url()
    message = f"{post.title} - {post_url}"
    graph.put_object(parent_object='me', connection_name='feed', message=message)
    post.is_shared_facebook = True
    post.save()

@shared_task
def share_to_whatsapp(post_id):
    post = BlogPost.objects.get(id=post_id)
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = f"New Blog Post: {post.title}\nRead here: {post.get_absolute_url()}"

    client.messages.create(
        from_='whatsapp:+13343800087',  # Twilio sandbox number
        body=message,
        to='whatsapp:+2348149492012'  # Replace with the recipient's number
    )
    post.is_shared_whatsapp = True
    post.save()

def schedule_social_sharing(post_id):
    # Schedule Twitter Sharing
    twitter_schedule, _ = IntervalSchedule.objects.get_or_create(
        every=5,  # Run every 5 minutes
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=twitter_schedule,
        name=f'Share post {post_id} on Twitter',
        task='blog.tasks.share_to_twitter',
        args=json.dumps([post_id]),
        start_time=timezone.now() + timedelta(minutes=5),
    )

    # Schedule Facebook Sharing
    facebook_schedule, _ = IntervalSchedule.objects.get_or_create(
        every=5,  # Run every 5 minutes
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=facebook_schedule,
        name=f'Share post {post_id} on Facebook',
        task='blog.tasks.share_to_facebook',
        args=json.dumps([post_id]),
        start_time=timezone.now() + timedelta(minutes=5),
    )

    # Schedule WhatsApp Sharing
    whatsapp_schedule, _ = IntervalSchedule.objects.get_or_create(
        every=5,  # Run every 5 minutes
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=whatsapp_schedule,
        name=f'Share post {post_id} on WhatsApp',
        task='blog.tasks.share_to_whatsapp',
        args=json.dumps([post_id]),
        start_time=timezone.now() + timedelta(minutes=5),
    )
