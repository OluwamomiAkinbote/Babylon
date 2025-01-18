from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta, datetime
from itertools import chain
import random

from blog.models import BlogPost, Category, Video, Trend
from advert.models import AdBanner, AdCategory
from blog.utils import insert_ad_banner
from shop.models import Product
from django.http import JsonResponse

def data_deletion(request):
    return JsonResponse({
        "url": "https://newstropy.com.ng/data-deletion",
        "message": "Data deletion request received. We will process your request shortly.",
    })


def video_reels(request):
    video_posts = Video.objects.all().order_by('-date')  
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')

    context = {
        'navbar_categories': navbar_categories,
        'video_posts': video_posts,
    }
    return render(request, 'pages/video_reels.html', context)


def more_stories(request):
    today = timezone.now() - timedelta(days=1)
    
    blogpost = BlogPost.objects.filter(date__lt=today).order_by('-date')
    trendpost = Trend.objects.filter(date__lt=today).order_by('-date')
    
    posts = sorted(
        chain(blogpost, trendpost),
        key=lambda post: post.date,
        reverse=True
    )

    paginator = Paginator(posts, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    trends = Trend.objects.all().order_by('-date')[:10]
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()

    context ={

        'page_obj': page_obj,
        'navbar_categories': navbar_categories,
        'trends': trends,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad,
        'sidebar_ad': sidebar_ad,
        'home_ad': home_ad,

    }

    return render(request, 'pages/more_stories.html', context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    
    all_other_category = BlogPost.objects.exclude(category=category).exclude(slug=slug)
    recommended_posts = random.sample(list(all_other_category), min(len(all_other_category), 5))

    blog_posts = BlogPost.objects.filter(category=category)
    video_posts = Video.objects.filter(category=category)
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()

    posts = sorted(
        chain(blog_posts, video_posts),
        key=lambda post: post.date if hasattr(post, 'date') else post.title,
        reverse=True
    )

    paginator = Paginator(posts, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={

        'posts': posts,
        'page_obj': page_obj,
        'category': category,
        'recommended_posts': recommended_posts,
        'navbar_categories': navbar_categories,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad,
        'sidebar_ad': sidebar_ad,
        'home_ad': home_ad,

    }

    return render(request, 'pages/category_list.html', context)


def trend_page(request):
    trend = Trend.objects.all().order_by('-date')
    posts = BlogPost.objects.all()
    recommended_posts = random.sample(list(posts), min(len(posts), 5))
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()

    paginator = Paginator(trend, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'trend': trend,
        'page_obj': page_obj,
        'recommended_posts': recommended_posts,
        'navbar_categories': navbar_categories,
        'leaderboard_ad': leaderboard_ad,
        'sidebar_ad': sidebar_ad,
        'home_ad': home_ad,
    }

    return render(request, 'pages/trend_page.html', context)


def privacy_policy(request):
    posts = BlogPost.objects.all()
    recommended_posts = random.sample(list(posts), min(len(posts), 5))

    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()

    context = {
        'recommended_posts': recommended_posts,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'navbar_categories': navbar_categories,
        'leaderboard_ad': leaderboard_ad,
        'sidebar_ad': sidebar_ad,
        'home_ad': home_ad,
    }

    return render(request, 'pages/privacy_policy.html', context)




def data_deletion(request):
    return JsonResponse({
        "url": "https://newstropy.com.ng/data-deletion",
        "message": "Data deletion request received. We will process your request shortly.",
    })
