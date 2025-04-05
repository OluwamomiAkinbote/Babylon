from datetime import timedelta
import random
from itertools import chain

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from advert.models import AdBanner
from shop.models import Product
from blog.models import BlogPost, Category, Trend, Video
from blog.serializers import BlogPostSerializer, VideoSerializer, TrendSerializer

class IndexAPIView(APIView):
    def get_category_posts(self, category_name, model=BlogPost, limit=None):
        """Fetch posts for a given category."""
        try:
            category = Category.objects.get(name=category_name)
            return model.objects.filter(category=category).order_by('-date')[:limit]
        except Category.DoesNotExist:
            return model.objects.none()

    def get(self, request):
        # Fetch video posts
        video_posts = self.get_category_posts('Videos', model=Video)

        # Fetch ads
        ads = {
            "leaderboard_ad": AdBanner.objects.filter(category='Leaderboard', active=True).first(),
            "sidebar_ad": AdBanner.objects.filter(category='Sidebar', active=True).first(),
            "home_ad": AdBanner.objects.filter(category='Home', active=True).first(),
        }

        # Fetch blog posts from five days ago
        five_days_ago = timezone.now() - timedelta(days=5)
        blog_posts_five_days_ago = BlogPost.objects.filter(date__lt=five_days_ago).order_by('-date')[:6]

        # Fetch shop products
        shop_products = Product.objects.all().order_by('?')[:12]

        # Prepare response data
        data = {
            "blog_posts_from_five_days_ago": BlogPostSerializer(blog_posts_five_days_ago, many=True).data,
            "categories": [category.name for category in Category.objects.all()],
            "video_posts": VideoSerializer(video_posts, many=True).data,
            "shop": [{"name": product.name, "price": product.price} for product in shop_products],
            "current_time": timezone.now(),
            "email": "contact@scodynatenews.com",
            "ads": {
                "leaderboard_ad": ads["leaderboard_ad"].image_large.url if ads["leaderboard_ad"] and ads["leaderboard_ad"].image_large else None,
                "sidebar_ad": ads["sidebar_ad"].image_small.url if ads["sidebar_ad"] and ads["sidebar_ad"].image_small else None,
                "home_ad": ads["home_ad"].image_large.url if ads["home_ad"] and ads["home_ad"].image_large else None,
            },
        }

        return Response(data)




class HeaderAPIView(APIView):
    def get(self, request):
        navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
        data = {
            "navbar_categories": [category.name for category in navbar_categories]
        }
        return Response(data)


class TrendAPIView(APIView):
    def get(self, request):
        # Fetch trending posts (latest 5)
        recent_trends = Trend.objects.all().order_by('-date')[:20]

        # Fetch posts from five days ago
        five_days_ago = timezone.now() - timedelta(days=5)
        old_trends = Trend.objects.filter(date__lt=five_days_ago).order_by('-date')[:6]

        data = {
            "recent_trends": TrendSerializer(recent_trends, many=True, context={"request": request}).data,
            "trend_posts_from_five_days_ago": TrendSerializer(old_trends, many=True, context={"request": request}).data,
        }

        return Response(data)


class GlobalNewsAPIView(APIView):
    def get(self, request):
        """Fetch Global News posts."""
        try:
            category = Category.objects.get(name='Global News')
            global_news_posts = BlogPost.objects.filter(category=category).order_by('-date')[:20]
        except Category.DoesNotExist:
            global_news_posts = BlogPost.objects.none()

        data = {
            "global_news_posts": BlogPostSerializer(global_news_posts, many=True).data,
        }
        return Response(data)


class SportsTechAPIView(APIView):
    def get(self, request):
        """Fetch Sports and Technology posts together."""
        try:
            sport_category = Category.objects.get(name='Sports')
            tech_category = Category.objects.get(name='Technology')

            sport_posts = BlogPost.objects.filter(category=sport_category).order_by('-date')[:5]
            tech_posts = BlogPost.objects.filter(category=tech_category).order_by('-date')[:5]
        except Category.DoesNotExist:
            sport_posts = BlogPost.objects.none()
            tech_posts = BlogPost.objects.none()

        data = {
            "sport_posts": BlogPostSerializer(sport_posts, many=True).data,
            "tech_posts": BlogPostSerializer(tech_posts, many=True).data,
        }
        return Response(data)



class MainExclusiveAPIView(APIView):
    def get_category_posts(self, category_name, limit=None):
        """Fetch posts for a given category."""
        try:
            category = Category.objects.get(name=category_name)
            return BlogPost.objects.filter(category=category).order_by('-date')[:limit], category
        except Category.DoesNotExist:
            return BlogPost.objects.none(), None

    def get(self, request):
        # Categories to exclude
        excluded_categories = Category.objects.filter(name__in=["Exclusive", "Global News"]).values_list("id", flat=True)

        # Fetch exclusive posts
        exclusive_posts, _ = self.get_category_posts('Exclusive', limit=20)

        # Fetch non-exclusive posts, excluding specified categories
        non_exclusive_posts = BlogPost.objects.exclude(category_id__in=excluded_categories).order_by('-date')[:20]

        # Select a random main post from combined posts
        combined_posts = list(chain(exclusive_posts, non_exclusive_posts))
        main_post = random.choice(combined_posts) if combined_posts else None

        # Prepare response data
        data = {
            "main_post": BlogPostSerializer(main_post).data if main_post else None,
            "exclusive_posts": BlogPostSerializer(exclusive_posts, many=True).data,
            "non_exclusive_posts": BlogPostSerializer(non_exclusive_posts, many=True).data,
        }

        return Response(data)




class HeroPostsAPIView(APIView):
    def get(self, request):
        """Fetch hero posts from exactly 3 days ago."""
        three_days_ago = timezone.now().date() - timedelta(days=3)

        hero_posts = BlogPost.objects.filter(
            date__date=three_days_ago  # Exact match for 3 days ago
        ).order_by('-date')[:5]

        return Response({
            "hero_posts": BlogPostSerializer(hero_posts, many=True).data
        })

