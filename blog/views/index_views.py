from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from random import choice, sample
from datetime import timedelta, datetime
from itertools import chain

from advert.models import AdBanner
from shop.models import Product
from blog.models import BlogPost, Category, Trend, Video  # assuming these are your models

def index(request):
    exclusive_category, global_news_category, videos_category = None, None, None

    # Query blog categories and posts
    try:
        exclusive_category = Category.objects.get(name='Exclusive')
        exclusive_posts = BlogPost.objects.filter(category=exclusive_category).order_by('-date')[:5]
    except Category.DoesNotExist:
        exclusive_posts = []

    try:
        global_news_category = Category.objects.get(name='Global News')
        global_news_posts = BlogPost.objects.filter(category=global_news_category).order_by('-date')[:6]
    except Category.DoesNotExist:
        global_news_posts = []

    try:
        videos_category = Category.objects.get(name='Videos')
        video_posts = Video.objects.filter(category=videos_category).order_by('-date')
    except Category.DoesNotExist:
        video_posts = []

    try:
        sport_category = Category.objects.get(name='Sports')
        sport_posts = BlogPost.objects.filter(category=sport_category).order_by('-date')[:5]
    except Category.DoesNotExist:
        sport_posts = []

    try:
        tech_category = Category.objects.get(name='Technology')
        tech_posts = BlogPost.objects.filter(category=tech_category).order_by('-date')[:6]
    except Category.DoesNotExist:
        tech_posts = []

    # Ads from the AdBanner model (leaderboard and sidebar)
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()

    five_days_ago = timezone.now() - timedelta(days=5)
    blogpost = BlogPost.objects.filter(date__lt=five_days_ago).order_by('-date')[:12]
    trendpost = Trend.objects.filter(date__lt=five_days_ago).order_by('-date')[:12]
    
    posts_from_five_days_ago = sorted(
        chain(blogpost, trendpost),
        key=lambda post: post.date,
        reverse=True
    )

    all_posts = BlogPost.objects.all().order_by('-date')
    three_days_ago = timezone.now() - timedelta(days=3)
    categories = Category.objects.all()
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')

    hero_posts = BlogPost.objects.filter(date__date=three_days_ago.date()).order_by('-date')
    if hero_posts.count() > 5:
        hero_posts = sample(list(hero_posts), 5)

    main_post = choice(all_posts) if all_posts.exists() else None

    non_exclusive_posts = all_posts.exclude(category=exclusive_category) if exclusive_category else all_posts
    non_exclusive_posts = non_exclusive_posts.exclude(category=global_news_category) if global_news_category else non_exclusive_posts
    trends = Trend.objects.all().order_by('-date')[:5]
    shop = Product.objects.all().order_by('?')[:12]

    # Context for the template
    context = {
        'main_post': main_post,
        'hero_posts': hero_posts,
        'non_exclusive_posts': non_exclusive_posts[:4],
        'exclusive_posts': exclusive_posts,
        'global_news_posts': global_news_posts,
        'posts_from_five_days_ago': posts_from_five_days_ago,
        'categories': categories,
        'navbar_categories': navbar_categories,
        'video_posts': video_posts,
        'sport_posts': sport_posts,
        'tech_posts': tech_posts,
        'trends': trends,
        'shop': shop,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad,  
        'home_ad': home_ad,  
    }

    return render(request, 'home/index.html', context)
