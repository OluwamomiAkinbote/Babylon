from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from itertools import chain
import random

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from blog.models import BlogPost, Category
from advert.models import AdBanner
from shop.models import Product
from blog.serializers import BlogPostSerializer


def get_common_context():
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()
    shop = Product.objects.all().order_by('?')[:10]
    
    return {
        'navbar_categories': list(navbar_categories.values()),
        'leaderboard_ad': leaderboard_ad.id if leaderboard_ad else None,
        'sidebar_ad': sidebar_ad.id if sidebar_ad else None,
        'home_ad': home_ad.id if home_ad else None,
        'shop': list(shop.values()),
        'email': 'contact@scodynatenews.com',
        'current_time': timezone.now()
    }




class MoreStoriesAPIView(APIView):
    def get(self, request):
        today = timezone.now() - timedelta(days=1)
        
        blogpost = BlogPost.objects.filter(date__lt=today).order_by('-date')
       
        
        posts = sorted(
            chain(blogpost),
            key=lambda post: post.date,
            reverse=True
        )

        paginator = Paginator(posts, 18)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'posts': list(page_obj.object_list.values()),
            'page_number': page_number,
            'has_next': page_obj.has_next(),
            **get_common_context()
        }
        return Response(context)


class CategoryListAPIView(APIView):
    def get(self, request, slug):
        # Get the main category
        category = get_object_or_404(Category, slug=slug)
        
        # Get all subcategories of this category
        subcategories = category.subcategories.all()
        
        # Get IDs of the main category and all its subcategories
        category_ids = [category.id] + list(subcategories.values_list('id', flat=True))
        
        # Get all posts from this category and its subcategories
        blog_posts = BlogPost.objects.filter(category_id__in=category_ids).order_by('-date')[:30]
        
        # Get recommended posts (excluding current category and its subcategories)
        all_other_category_posts = BlogPost.objects.exclude(category_id__in=category_ids)
        recommended_posts = random.sample(
            list(all_other_category_posts), 
            min(len(all_other_category_posts), 5)
        )

        # Serialize the data
        context = {
            'category': {
                'name': category.name,
                'slug': category.slug,
                'description': getattr(category, 'description', ''),
            },
            'subcategories': [
                {
                    'name': sub.name,
                    'slug': sub.slug,
                    'description': getattr(sub, 'description', ''),
                } 
                for sub in subcategories
            ],
            'posts': BlogPostSerializer(blog_posts, many=True).data,
            'recommended_posts': BlogPostSerializer(recommended_posts, many=True).data,
            **get_common_context()
        }
        
        return Response(context)





class PrivacyPolicyAPIView(APIView):
    def get(self, request):
        posts = BlogPost.objects.all()
        recommended_posts = random.sample(list(posts), min(len(posts), 5))

        context = {
            'recommended_posts': list(recommended_posts),
            **get_common_context()
        }
        return Response(context)


class DataDeletionAPIView(APIView):
    def get(self, request):
        return Response({
            "url": "https://newstropy.com.ng/data-deletion",
            "message": "Data deletion request received. We will process your request shortly."
        })
