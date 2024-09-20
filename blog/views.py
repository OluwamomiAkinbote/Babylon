from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from random import choice, sample
from .models import BlogPost, Category, Video, Trend, Subscription
from datetime import timedelta, datetime
from django.http import JsonResponse
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from itertools import chain
import random
from advert.models import AdBanner, AdCategory
from .utils import insert_ad_banner
from django.http import JsonResponse
from django.db.models import Q
from .models import BlogPost, Trend


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
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad,  
        'home_ad': home_ad,  
    }

    return render(request, 'index.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    related_posts = BlogPost.objects.filter(category=post.category).exclude(slug=slug)[:5]
    all_other_posts = BlogPost.objects.exclude(category=post.category).exclude(slug=slug)
    recommended_posts = random.sample(list(all_other_posts), min(len(all_other_posts), 5))

    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()

    # Retrieve active ads and group them by category
    ads = AdBanner.objects.filter(category=AdCategory.INLINE, active=True)

    # Insert ads dynamically into the post content
    advert_content = insert_ad_banner(post.content, ads)

    context = {
        'post': post,
        'related_posts': related_posts,
        'recommended_posts': recommended_posts,
        'navbar_categories': navbar_categories,
        'advert': advert_content,
        'current_time': timezone.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad, 
    }
    
    return render(request, 'blog_detail.html', context)



def video_detail(request, slug):
    video = get_object_or_404(Video, slug=slug)
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    trends = Trend.objects.all().order_by('-date')[:10]
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
        # Retrieve active ads and group them by category
    ads = AdBanner.objects.filter(category=AdCategory.INLINE, active=True)

    # Insert ads dynamically into the post content
    advert_content = insert_ad_banner(video.description, ads)

    return render(request, 'video_details.html', {
        'video': video,
        'navbar_categories': navbar_categories,
        'trends': trends,
        'advert': advert_content,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad, 
    })


def more_stories(request):
    today=timezone.now() - timedelta(days=1)
    
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

    return render(request, 'more_stories.html', {
        'page_obj': page_obj,
        'navbar_categories': navbar_categories,
        'trends': trends,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad, 
    })


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')

    blog_posts = BlogPost.objects.filter(category=category)
    video_posts = Video.objects.filter(category=category)
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()

    posts = sorted(
        chain(blog_posts, video_posts),
        key=lambda post: post.date if hasattr(post, 'date') else post.title,
        reverse=True
    )

    paginator = Paginator(posts, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'category_list.html', {
        'posts': posts,
        'page_obj': page_obj,
        'category': category,
        'navbar_categories': navbar_categories,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad, 
    })


def subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)

        if not name or not email:
            return JsonResponse({'error': "Please provide a valid name and email to subscribe."}, status=400)

        if get_user_model().objects.filter(email=email).exists():
            return JsonResponse({'error': f"The email {email} is already associated with a registered user."}, status=400)

        if Subscription.objects.filter(email=email).exists():
            return JsonResponse({'error': f"The email {email} is already subscribed."}, status=400)

        try:
            validate_email(email)
        except ValidationError as e:
            return JsonResponse({'error': e.messages[0]}, status=400)

        Subscription.objects.create(name=name, email=email)
        return JsonResponse({'success': True, 'message': f'Thank you, {name}! You have successfully subscribed.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def search_view(request):
    query = request.GET.get('query', '')
    
    # Perform a single query with both title and content using Q objects for BlogPost
    blogpost_results = BlogPost.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    
    # Perform a single query with both title and content using Q objects for Trend
    trend_results = Trend.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    
    # Combine the two querysets as lists
    results = list(blogpost_results) + list(trend_results)
    

    paginator = Paginator(results, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    trends = Trend.objects.all().order_by('-date')[:10]
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()

    return render(request, 'search_results.html', {
        'results': results,
        'query': query,
        'trends': trends,
        'page_obj': page_obj,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'navbar_categories': navbar_categories,
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad, 
    })



def get_suggestions(request):
    query = request.GET.get('query', '')

    if query:
        # Fetch BlogPost and Trend titles that match the query
        blogpost_suggestions = BlogPost.objects.filter(
            Q(title__icontains=query)
        ).values_list('title', flat=True)[:5]  # Limit to 5 results from BlogPost

        trend_suggestions = Trend.objects.filter(
            Q(title__icontains=query)
        ).values_list('title', flat=True)[:5]  # Limit to 5 results from Trend

        # Combine both suggestions into a single list
        suggestions = list(blogpost_suggestions) + list(trend_suggestions)
    else:
        suggestions = []

    return JsonResponse(suggestions, safe=False)



def trend_detail(request, slug):
    trend = get_object_or_404(Trend, slug=slug)
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    
    ads = AdBanner.objects.filter(active=True)

    advert_content = insert_ad_banner(trend.content, ads)

    return render(request, 'trend_detail.html', {
        'trend': trend,
        'advert':advert_content,
        'current_time': datetime.now(),
        'email': 'contact@scodynatenews.com',
        'navbar_categories': navbar_categories,
        'leaderboard_ad': leaderboard_ad, 
        'sidebar_ad': sidebar_ad, 
    })
