from datetime import timedelta
import random
from itertools import chain
from django.db.models import Q

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from advert.models import AdBanner
from shop.models import Product
from blog.models import BlogPost, Category, Trend
from blog.serializers import BlogPostSerializer, TrendSerializer

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
        navbar_categories = Category.objects.filter(
            show_on_navbar=True, 
            parent__isnull=True
        ).order_by('priority')

        categories_data = []
        for category in navbar_categories:
            subcategories = category.subcategories.all()
            subcategory_ids = list(subcategories.values_list('id', flat=True))
            subcategory_ids.append(category.id)

            latest_posts = BlogPost.objects.filter(
                category_id__in=subcategory_ids
            ).order_by('-date')[:4]

            categories_data.append({
                'name': category.name,
                'slug': category.slug,
                'has_subcategories': subcategories.exists(),
                'subcategories': [
                    {'name': sub.name, 'slug': sub.slug}
                    for sub in subcategories.order_by('priority')
                ],
                'latest_posts': BlogPostSerializer(latest_posts, many=True).data
            })

        return Response({
            "navbar_categories": categories_data
        })



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
        try:
            # Get parent category and its subcategories
            global_news = Category.objects.get(name='Global News')
            subcategories = global_news.subcategories.all()
            category_ids = [global_news.id] + [sub.id for sub in subcategories]

            # Fetch posts from parent + subcategories
            posts = BlogPost.objects.filter(
                category__id__in=category_ids
            ).order_by('-date')[:20]

        except Category.DoesNotExist:
            posts = BlogPost.objects.none()

        return Response({
            "global_news_posts": BlogPostSerializer(posts, many=True).data,
            # Optional: Include subcategory breakdown
            "subcategories": [sub.name for sub in subcategories]
        })

class SportsTechAPIView(APIView):
    def get(self, request):
        """Fetch Sports and Technology posts together, including their subcategories."""
        try:
            # Get Sports category and its subcategories
            sport_category = Category.objects.get(name='Sports')
            sport_subcategories = sport_category.subcategories.all()
            sport_category_ids = [sport_category.id] + [sub.id for sub in sport_subcategories]
            
            # Get Technology category and its subcategories
            tech_category = Category.objects.get(name='Technology')
            tech_subcategories = tech_category.subcategories.all()
            tech_category_ids = [tech_category.id] + [sub.id for sub in tech_subcategories]

            # Get posts for both categories including their subcategories
            sport_posts = BlogPost.objects.filter(category__id__in=sport_category_ids).order_by('-date')[:5]
            tech_posts = BlogPost.objects.filter(category__id__in=tech_category_ids).order_by('-date')[:5]
            
        except Category.DoesNotExist:
            sport_posts = BlogPost.objects.none()
            tech_posts = BlogPost.objects.none()

        data = {
            "sport_posts": BlogPostSerializer(sport_posts, many=True).data,
            "tech_posts": BlogPostSerializer(tech_posts, many=True).data,
        }
        return Response(data)








class FeaturedCategoryPostsView(APIView):
    def get(self, request):
        parent_categories = ['Business', 'Entertainment', 'Health', 'Energy']
        data = {}

        for parent_name in parent_categories:
            try:
                # Get parent category
                parent = Category.objects.get(name__iexact=parent_name)

                # Get all subcategories
                subcategories = parent.subcategories.all()

                # Collect category IDs: parent + its subcategories
                category_ids = [parent.id] + [sub.id for sub in subcategories]

                # Filter posts that belong to any of these categories
                posts = BlogPost.objects.filter(category__id__in=category_ids).order_by('-date')[:2]

                serializer = BlogPostSerializer(posts, many=True, context={'request': request})
                data[parent_name] = serializer.data

            except Category.DoesNotExist:
                data[parent_name] = []

        return Response(data)




class MainExclusiveAPIView(APIView):
    def get(self, request):
        try:
            # Get main categories and their subcategories
            politics_category = Category.objects.get(name__iexact='Politics')
            exclusive_category = Category.objects.get(name__iexact='Exclusive')
            
            # Get all subcategories for each main category
            politics_subcategories = politics_category.subcategories.all()
            exclusive_subcategories = exclusive_category.subcategories.all()
            
            # Collect all relevant category IDs
            politics_category_ids = [politics_category.id] + [sub.id for sub in politics_subcategories]
            exclusive_category_ids = [exclusive_category.id] + [sub.id for sub in exclusive_subcategories]

        except Category.DoesNotExist:
            return Response({'error': 'Required categories not found.'}, status=404)

        # Get posts including those from subcategories
        politics_queryset = BlogPost.objects.filter(
            category__id__in=politics_category_ids
        ).order_by('-date')[:20]
        
        exclusive_queryset = BlogPost.objects.filter(
            category__id__in=exclusive_category_ids
        ).order_by('-date')[:20]

        # Combine posts for random main post selection
        combined_posts = list(politics_queryset) + list(exclusive_queryset)
        main_post = random.choice(combined_posts) if combined_posts else None

        return Response({
            'main_post': BlogPostSerializer(main_post, context={'request': request}).data if main_post else None,
            'politics_posts': BlogPostSerializer(politics_queryset, many=True, context={'request': request}).data,
            'exclusive_posts': BlogPostSerializer(exclusive_queryset, many=True, context={'request': request}).data,
        })



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

