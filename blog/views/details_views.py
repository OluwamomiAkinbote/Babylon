from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.templatetags.static import static
import random
from blog.models import BlogPost, Category, Trend
from advert.models import AdBanner, AdCategory
from blog.utils import insert_ad_banner
from shop.models import Product
from blog.serializers import BlogPostSerializer, TrendSerializer, CategorySerializer 

from advert.serializers import AdBannerSerializer  # Import the serializer

def get_common_context():
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by("priority")
    leaderboard_ad = AdBanner.objects.filter(category="Leaderboard", active=True).first()
    sidebar_ad = AdBanner.objects.filter(category="Sidebar", active=True).first()
    home_ad = AdBanner.objects.filter(category="Home", active=True).first()
    ads = AdBanner.objects.filter(category=AdCategory.INLINE, active=True)

    return {
        "navbar_categories": CategorySerializer(navbar_categories, many=True).data,
        "leaderboard_ad": AdBannerSerializer(leaderboard_ad).data if leaderboard_ad else None,
        "sidebar_ad": AdBannerSerializer(sidebar_ad).data if sidebar_ad else None,
        "home_ad": AdBannerSerializer(home_ad).data if home_ad else None,
        "ads": AdBannerSerializer(ads, many=True).data,
        "email": "contact@scodynatenews.com",
        "current_time": timezone.now(),
    }


class BlogDetailAPIView(APIView):
    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug)

        related_posts = BlogPost.objects.filter(category=post.category).exclude(slug=slug)[:5]
        recommended_posts = BlogPost.objects.exclude(category=post.category).exclude(slug=slug)[:5]

        fallback_image_url = request.build_absolute_uri(static("images/seo-logo.png"))

        # Check if the post has media
        media_items = post.media.all()
        absolute_image_url = fallback_image_url  # Default image

        for media_item in media_items:
            if media_item.media and media_item.media.url:
                if media_item.media.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heif', '.heic')): 
                    # Check if the media item is an image
                    absolute_image_url = request.build_absolute_uri(media_item.media.url)
                    break  # Stop the loop once we find an image

        # Get common context
        common_context = get_common_context()
        # Generate advert content
        advert_content = insert_ad_banner(post.content, common_context["ads"])

        # SEO data
        seo_data = {
            "title": post.title,
            "description": advert_content[:20],  # Use advert_content as the description
            "image_url": absolute_image_url,
            "url": request.build_absolute_uri(post.get_absolute_url())
        }

        response_data = {
            "post": BlogPostSerializer(post).data,
            "related_posts": BlogPostSerializer(related_posts, many=True).data,
            "recommended_posts": BlogPostSerializer(recommended_posts, many=True).data,
            "advert": advert_content,
            "seo": seo_data,  # Include SEO data with advert content as description
            **common_context,
        }

        return Response(response_data)




class TrendDetailAPIView(APIView):
    def get(self, request, slug):
        trend = get_object_or_404(Trend, slug=slug)

        posts = list(BlogPost.objects.all())
        random.shuffle(posts)
        recommended_posts = posts[:5]

        common_context = get_common_context()
        advert_content = insert_ad_banner(trend.content, common_context["ads"])

        absolute_file_url = request.build_absolute_uri(trend.get_file_url()) if (trend.is_image or trend.is_video) else None

        return Response(
            {
                "trend": TrendSerializer(trend).data,
                "recommended_posts": BlogPostSerializer(recommended_posts, many=True).data,
                "advert": advert_content,
                "absolute_file_url": absolute_file_url,
                **common_context,
            }
        )


