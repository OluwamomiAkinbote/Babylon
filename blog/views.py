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
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

def index(request):
    exclusive_category = None
    global_news_category = None
    videos_category = None

    try:
        # Fetching the exclusive category by its name
        exclusive_category = Category.objects.get(name='Exclusive')
        exclusive_posts = BlogPost.objects.filter(category=exclusive_category).order_by('-date')[:5]
    except Category.DoesNotExist:
        exclusive_posts = []

    try:
        # Fetching the global news category by its name
        global_news_category = Category.objects.get(name='Global News')
        global_news_posts = BlogPost.objects.filter(category=global_news_category).order_by('-date')[:6]
    except Category.DoesNotExist:
        global_news_posts = []
    
    try: 
        videos_category = Category.objects.get(name='Videos')
        video_posts = Video.objects.filter(category=videos_category).order_by('-title')
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

    # Ensure all post dates are timezone-aware
    for post in all_posts:
        if not timezone.is_aware(post.date):
            post.date = timezone.make_aware(post.date, timezone.get_current_timezone())

    context = {
        'main_post': main_post,
        'hero_posts': hero_posts,
        'non_exclusive_posts': non_exclusive_posts[:4],  # Limit to 4 posts
        'exclusive_posts': exclusive_posts,
        'global_news_posts': global_news_posts,
        'categories': categories,
        'navbar_categories': navbar_categories,
        'video_posts': video_posts,
        'sport_posts': sport_posts,
        'tech_posts': tech_posts,
    }

    return render(request, 'index.html', context)



def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments.filter(parent_comment=None)  # Fetch top-level comments only

    related_posts = BlogPost.objects.filter(category=post.category).exclude(slug=slug)[:5]
    all_other_posts = BlogPost.objects.exclude(category=post.category).exclude(slug=slug)
    recommended_posts = random.sample(list(all_other_posts), min(len(all_other_posts), 5))

    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')


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
            return redirect('blog_detail', slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'navbar_categories': navbar_categories,
        'related_posts': related_posts,
        'recommended_posts': recommended_posts,
    
    })



def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog_detail', slug=post.slug)  # Redirect to the post detail page using slug
    else:
        form = CommentForm()

    return redirect('blog_detail', slug=post.slug)  # Redirect to the post detail page using slug


def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.post = parent_comment.post  # Assuming Comment has a ForeignKey to BlogPost
            new_reply.parent_comment = parent_comment
            new_reply.save()
            return redirect('blog_detail', slug=parent_comment.post.slug)  # Redirect to post detail page using slug
    else:
        form = CommentForm()

    return redirect('blog_detail', slug=parent_comment.post.slug) 

@login_required
def like_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to like comments.'}, status=403)

    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        data = json.loads(request.body)
        liked = data.get('liked', False)
        
        if liked:
            if request.user not in comment.liked_by.all():
                comment.liked_by.add(request.user)
                comment.likes_count += 1
        else:
            if request.user in comment.liked_by.all():
                comment.liked_by.remove(request.user)
                comment.likes_count -= 1
        
        comment.save()
        return JsonResponse({'likes_count': comment.likes_count})

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(category=category)
    return render(request, 'category_list.html', {'category': category, 'posts': posts})

def subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)

        # Validate the input
        if not name or not email:
            return JsonResponse({'error': "Please provide a valid name and email to subscribe."}, status=400)

        # Check if the email is already associated with a registered user
        if get_user_model().objects.filter(email=email).exists():
            return JsonResponse({'error': f"The email {email} is already associated with a registered user. Please log in to subscribe or unsubscribe."}, status=400)

        # Check if the email is already subscribed
        if Subscription.objects.filter(email=email).exists():
            return JsonResponse({'error': f"The email {email} is already subscribed."}, status=400)

        # Validate the email format
        try:
            validate_email(email)
        except ValidationError as e:
            return JsonResponse({'error': e.messages[0]}, status=400)

        # Create and save the subscription
        Subscription.objects.create(name=name, email=email)
        return JsonResponse({'success': True, 'message': f'Thank you, {name}! You have successfully subscribed with the email {email}.'})

    # If the request is not POST, return an error
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


