from django.shortcuts import render
from django.utils import timezone
from random import choice, sample
from datetime import timedelta, datetime
from itertools import chain

from advert.models import AdBanner
from shop.models import Product
from blog.models import BlogPost, Category, Trend, Video
from django.utils import timezone




def index(request):
    local_time = timezone.localtime(timezone.now())
    
    
    def get_category_posts(category_name, model=BlogPost, limit=None):
        try:
            category = Category.objects.get(name=category_name)
            return model.objects.filter(category=category).order_by('-date')[:limit], category
        except Category.DoesNotExist:
            return model.objects.none(), None

    # Fetch posts by category
    exclusive_posts, exclusive_category = get_category_posts('Exclusive', limit=5)
    global_news_posts, global_news_category = get_category_posts('Global News', limit=6)
    sport_posts, _ = get_category_posts('Sports', limit=5)
    tech_posts, _ = get_category_posts('Technology', limit=6)
    video_posts, _ = get_category_posts('Videos', model=Video)

    # Fetch ads
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()

    # Aggregate posts
    five_days_ago = timezone.now() - timedelta(days=5)
    posts_from_five_days_ago = sorted(
        chain(
            BlogPost.objects.filter(date__lt=five_days_ago).order_by('-date')[:12],
            Trend.objects.filter(date__lt=five_days_ago).order_by('-date')[:12]
        ),
        key=lambda post: post.date,
        reverse=True
    )

    # Hero posts
    three_days_ago = timezone.now() - timedelta(days=3)
    hero_posts = BlogPost.objects.filter(date__date=three_days_ago.date()).order_by('-date')[:5]

    # Exclude categories for non-exclusive posts
    all_posts = BlogPost.objects.all().order_by('-date')
    non_exclusive_posts = all_posts.exclude(category__in=filter(None, [exclusive_category, global_news_category]))[:4]

    # Combine exclusive and non-exclusive posts for random selection
    combined_posts = list(chain(exclusive_posts, non_exclusive_posts))
    main_post = choice(combined_posts) if combined_posts else None

    # Other data
    trends = Trend.objects.all().order_by('-date')[:5]
    shop = Product.objects.all().order_by('?')[:12]
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')

    # Context
    context = {
        'main_post': main_post,
        'hero_posts': list(hero_posts),
        'non_exclusive_posts': non_exclusive_posts,
        'exclusive_posts': exclusive_posts,
        'global_news_posts': global_news_posts,
        'posts_from_five_days_ago': posts_from_five_days_ago,
        'categories': Category.objects.all(),
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
