from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from random import sample
from blog.models import BlogPost, Category, Video, Trend
from datetime import datetime
from advert.models import AdBanner, AdCategory
from blog.utils import insert_ad_banner
from shop.models import Product
import random


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    related_posts = BlogPost.objects.filter(category=post.category).exclude(slug=slug)[:5]
    all_other_posts = BlogPost.objects.exclude(category=post.category).exclude(slug=slug)
    recommended_posts = random.sample(list(all_other_posts), min(len(all_other_posts), 5))

    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()

    # Retrieve active ads and group them by category
    ads = AdBanner.objects.filter(category=AdCategory.INLINE, active=True)

    # Insert ads dynamically into the post content
    advert_content = insert_ad_banner(post.content, ads)
    shop = Product.objects.all().order_by('?')[:10]

    context = {
        'post': post,
        'related_posts': related_posts,
        'recommended_posts': recommended_posts,
        'navbar_categories': navbar_categories,
        'advert': advert_content,
        'shop': shop,
        'current_time': timezone.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad, 
        'home_ad': home_ad, 
    }
    
    return render(request, 'blog_details/blog_detail.html', context)


def video_detail(request, slug):
    video = get_object_or_404(Video, slug=slug)
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    trends = Trend.objects.all().order_by('-date')[:10]
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()

    # Retrieve active ads and group them by category
    ads = AdBanner.objects.filter(category=AdCategory.INLINE, active=True)

    # Insert ads dynamically into the post content
    advert_content = insert_ad_banner(video.description, ads)

    context ={

        'video': video,
        'navbar_categories': navbar_categories,
        'trends': trends,
        'advert': advert_content,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad,
        'home_ad': home_ad, 

    }

    return render(request, 'blog_details/video_details.html', context)


def trend_detail(request, slug):
    trend = get_object_or_404(Trend, slug=slug)

    posts = BlogPost.objects.all()
    recommended_posts = random.sample(list(posts), min(len(posts), 5))
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()
    
    ads = AdBanner.objects.filter(active=True)

    advert_content = insert_ad_banner(trend.content, ads)
    shop = Product.objects.all().order_by('?')[:12]

    context = {

        'trend': trend,
        'advert': advert_content,
        'shop': shop,
        'recommended_posts': recommended_posts,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'navbar_categories': navbar_categories,
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad,
        'home_ad': home_ad, 

    }

    return render(request, 'blog_details/trend_detail.html', context)
