import tweepy
from django.core.management.base import BaseCommand
from blog.models import BlogPost
from django.conf import settings

class Command(BaseCommand):
    help = 'Post new blog posts to Twitter'

    def handle(self, *args, **options):
        # Use the API credentials from settings
        api_key = settings.TWITTER_API_KEY
        api_secret = settings.TWITTER_API_SECRET_KEY
        access_token = settings.TWITTER_ACCESS_TOKEN
        access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        posts = BlogPost.objects.filter(tweeted=False).order_by('-date')[:30]  # Get latest posts

        for post in posts:
            try:
                tweet_text = f"{post.title[:200]}...\nRead more: https://www.newstropy.online{post.get_absolute_url()}"

                # Get the first media associated with the post (if any)
                first_media = post.media.first()

                if first_media and first_media.media:
                    media_path = first_media.media.path  # Local path to the file
                    # Upload media to Twitter
                    res = api.media_upload(media_path)
                    media_ids = [res.media_id]

                    # Post tweet with media
                    api.update_status(status=tweet_text, media_ids=media_ids)
                else:
                    # Post tweet without media
                    api.update_status(status=tweet_text)

                # Mark post as tweeted
                post.tweeted = True
                post.save()

                self.stdout.write(self.style.SUCCESS(f"Tweeted: {post.title}"))
            except Exception as e:
                self.stderr.write(f"Failed to tweet: {post.title} | Error: {e}")
