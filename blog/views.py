from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from random import choice, sample
from .models import BlogPost, Category, Comment, Media, Video
from datetime import timedelta
from .forms import CommentForm
import random
from .models import Subscription
from .forms import SubscriptionForm
from django.http import JsonResponse

def index(request):
    exclusive_category = None
    global_news_category = None
    videos_category = None

    try:
        # Fetching the exclusive category by its name
        exclusive_category = Category.objects.get(name='Exclusive')
        exclusive_posts = BlogPost.objects.filter(category=exclusive_category)
    except Category.DoesNotExist:
        exclusive_posts = []

    try:
        # Fetching the global news category by its name
        global_news_category = Category.objects.get(name='Global News')
        global_news_posts = BlogPost.objects.filter(category=global_news_category).order_by('-date')[:6]
    except Category.DoesNotExist:
        global_news_posts = []
    
    # Global news category

    try: 
        videos_category = Category.objects.get(name='Videos')
        video_posts = Video.objects.filter(category=videos_category).order_by('-title')
    except Category.DoesNotExist:
        video_posts = []
    
    # sports category

    try:
        sport_category = Category.objects.get(name='Sports')
        sport_posts = BlogPost.objects.filter(category=sport_category).order_by('-date')[:6]
    except Category.DoesNotExist:
        sport_posts = []

    try:
        tech_category = Category.objects.get(name='Technology')
        tech_posts = BlogPost.objects.filter(category=tech_category).order_by('-date')[:6]
    except Category.DoesNotExist:
        tech_posts = []

    # Fetch all posts and other categories
    all_posts = BlogPost.objects.all().order_by('-date')
    three_days_ago = timezone.now() - timedelta(days=3)
    categories = Category.objects.all()
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')

    # Filter posts to include only those exactly 3 days old
    hero_posts = BlogPost.objects.filter(date__date=three_days_ago.date()).order_by('-date')
    # Select up to 5 random posts from the filtered hero posts
    if hero_posts.count() > 5:
        hero_posts = sample(list(hero_posts), 5)

    # Select a random main post from any category
    main_post = choice(all_posts) if all_posts.exists() else None

    # Exclude exclusive posts for the "Other Posts" section
    non_exclusive_posts = all_posts.exclude(category=exclusive_category) if exclusive_category else all_posts

    # Exclude global news posts for the "Other Posts" section
    non_exclusive_posts = non_exclusive_posts.exclude(category=global_news_category) if global_news_category else non_exclusive_posts

    # Pagination for non-exclusive posts
    paginator_non_exclusive = Paginator(non_exclusive_posts, 4)  # Show 4 posts per page
    page_number_non_exclusive = request.GET.get('page_non_exclusive')
    page_obj_non_exclusive = paginator_non_exclusive.get_page(page_number_non_exclusive)

    # Pagination for exclusive posts
    paginator_exclusive = Paginator(exclusive_posts, 7)  # Show 7 exclusive posts per page
    page_number_exclusive = request.GET.get('page_exclusive')
    page_obj_exclusive = paginator_exclusive.get_page(page_number_exclusive)

    # Pagination for global news posts
    paginator_global_news = Paginator(global_news_posts, 5)  # Show 5 global news posts per page
    page_number_global_news = request.GET.get('page_global_news')
    page_obj_global_news = paginator_global_news.get_page(page_number_global_news)

    # Ensure the correct page_obj is used based on the URL query parameter
    if page_number_exclusive:
        page_obj = page_obj_exclusive
    elif page_number_global_news:
        page_obj = page_obj_global_news
    else:
        page_obj = page_obj_non_exclusive

    # Ensure all post dates are timezone-aware
    for post in all_posts:
        if not timezone.is_aware(post.date):
            post.date = timezone.make_aware(post.date, timezone.get_current_timezone())

    context = {
        'main_post': main_post,
        'hero_posts': hero_posts,
        'page_obj_non_exclusive': page_obj_non_exclusive,
        'page_obj_exclusive': page_obj_exclusive,
        'page_obj_global_news': page_obj_global_news,
        'categories': categories,
        'navbar_categories': navbar_categories,
        'exclusive_posts': exclusive_posts,
        'global_news_posts': global_news_posts,
        'other_posts': page_obj_non_exclusive,
        'video_posts': video_posts,
        'sport_posts': sport_posts,
        'tech_posts': tech_posts,
    }

    return render(request, 'index.html', context)



def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.filter(parent_comment=None)  # Fetch top-level comments only

    related_posts = BlogPost.objects.filter(category=post.category).exclude(pk=pk)[:5]
    all_other_posts = BlogPost.objects.exclude(category=post.category).exclude(pk=pk)
    recommended_posts = random.sample(list(all_other_posts), min(len(all_other_posts), 5))

    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    absolute_image_url = request.build_absolute_uri(post.image.url) if post.image else None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_comment_id = form.cleaned_data.get('parent_comment_id')
            if parent_comment_id:
                parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
                new_reply = form.save(commit=False)
                new_reply.post = post
                new_reply.parent_comment = parent_comment
                new_reply.save()
            else:
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'navbar_categories': navbar_categories,
        'related_posts': related_posts,
        'recommended_posts': recommended_posts,
        'absolute_image-url':absolute_image_url
    })

def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog_detail', pk=post.pk)  # Redirect to the post detail page
    else:
        form = CommentForm()

    # Handle form errors or display the form again with errors
    return redirect('blog_detail', pk=post.pk)  # Redirect


def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.post = parent_comment.post  # Assuming Comment has a ForeignKey to BlogPost
            new_reply.parent_comment = parent_comment
            new_reply.save()
            return redirect('blog_detail', pk=parent_comment.post.pk)  # Redirect to post detail page
    else:
        form = CommentForm()

    return redirect('blog_detail', pk=parent_comment.post.pk) 

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(category=category)
    return render(request, 'category_list.html', {'category': category, 'posts': posts})


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Thank you for subscribing!'})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)