from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.templatetags.static import static
import random
from blog.models import BlogPost, Category
from advert.models import AdBanner, AdCategory
from blog.utils import inject_banner
from shop.models import Product
from blog.serializers import BlogPostSerializer, CategorySerializer 

from advert.serializers import AdBannerSerializer  # Import the serializer

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils.html import strip_tags



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


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class NewsListView(ListAPIView):
    """
    Basic API endpoint that lists all news posts
    """
    serializer_class = BlogPostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = BlogPost.objects.all().order_by('-date')
        
        # Optional category filter
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
            
        return queryset

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'request': self.request
        }



class BlogDetailAPIView(APIView):
    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug)

                # 
        category_ids = [post.category.id] + [sub.id for sub in post.category.subcategories.all()]

        # Get related posts from category and subcategories
        related_posts = BlogPost.objects.filter(category__id__in=category_ids).exclude(slug=slug).order_by('-date')[:5]
        recommended_posts = BlogPost.objects.exclude(category=post.category).exclude(slug=slug).order_by('-date')[:5]

        # Fallback static image
        fallback_image_url = request.build_absolute_uri(static("images/Breakingnews.png"))

        # Use seo_image if available, otherwise fallback
        if post.seo_image and post.seo_image.url:
            absolute_image_url = request.build_absolute_uri(post.seo_image.url)
        else:
            absolute_image_url = fallback_image_url

        # Common context
        common_context = get_common_context()

        # Insert ad banner into content
        advert_content = inject_banner(post.content)
        
        clean_lead = strip_tags(post.lead) if post.lead else None

        # Improved SEO data
        seo_data = {
            "title": post.title,
            "description": clean_lead if clean_lead else strip_tags(advert_content)[:160],   
            "image_url": absolute_image_url,
            "url": request.build_absolute_uri(post.get_absolute_url()),
            "date": post.date.isoformat() if post.date else None,  # Add publication date
            "type": "article",            
        }

        response_data = {
            "post": BlogPostSerializer(post).data,
            "related_posts": BlogPostSerializer(related_posts, many=True).data,
            "recommended_posts": BlogPostSerializer(recommended_posts, many=True).data,
            "advert": advert_content,
            "seo": seo_data,
            **common_context,
        }

        return Response(response_data)







