from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from random import sample
from blog.models import BlogPost, Category, Video, Trend
from advert.models import AdBanner, AdCategory
from blog.utils import insert_ad_banner
from shop.models import Product
import random
from django.templatetags.static import static

def get_common_context():
    
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()
    ads = AdBanner.objects.filter(category=AdCategory.INLINE, active=True)
    shop = Product.objects.all().order_by('?')[:10]
    
    return {
        'navbar_categories': navbar_categories,
        'leaderboard_ad': leaderboard_ad,
        'sidebar_ad': sidebar_ad,
        'home_ad': home_ad,
        'ads': ads,
        'shop': shop,
        'email': 'contact@scodynatenews.com',
        'current_time': timezone.now()
    }

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    related_posts = BlogPost.objects.filter(category=post.category).exclude(slug=slug)[:5]
    all_other_posts = BlogPost.objects.exclude(category=post.category).exclude(slug=slug)

    # Fallback image URL
    fallback_image_url = request.build_absolute_uri(static('images/Breakingnews.png'))
    try:
        absolute_image_url = request.build_absolute_uri(post.image.url)
    except AttributeError:
        absolute_image_url = fallback_image_url

    recommended_posts = random.sample(list(all_other_posts), min(len(all_other_posts), 5))

    common_context = get_common_context()
    advert_content = insert_ad_banner(post.content, common_context['ads'])

    context = {
        'post': post,
        'related_posts': related_posts,
        'recommended_posts': recommended_posts,
        'advert': advert_content,
        'absolute_image_url': absolute_image_url,
        **common_context
    }

    return render(request, 'blog_details/blog_detail.html', context)








def trend_detail(request, slug):
    trend = get_object_or_404(Trend, slug=slug)
    posts = BlogPost.objects.all()
    recommended_posts = sample(list(posts), min(len(posts), 5))
    common_context = get_common_context()
    advert_content = insert_ad_banner(trend.content, common_context['ads'])

    # Use get_file_url() or get_absolute_file_url() depending on the content type
    if trend.is_image or trend.is_video:
        absolute_file_url = request.build_absolute_uri(trend.get_file_url())  # For both images and videos
    else:
        absolute_file_url = None  # Or a default fallback URL

    # Final Open Graph URL adjustments
    og_file_url = absolute_file_url

    context = {
        'trend': trend,
        'recommended_posts': recommended_posts,
        'advert': advert_content,
        'absolute_file_url': og_file_url,  # Pass the Open Graph URL
        **common_context
    }

    return render(request, 'blog_details/trend_detail.html', context)




def video_detail(request, slug):
    video = get_object_or_404(Video, slug=slug)
    trends = Trend.objects.all().order_by('-date')[:10]

    common_context = get_common_context()
    advert_content = insert_ad_banner(video.description, common_context['ads'])
    
    fallback_image_url = request.build_absolute_uri(static('images/Breakingnews.png'))
    try:
        absolute_video_url = request.build_absolute_uri(video.file.url)
    except AttributeError:
        absolute_video_url = fallback_image_url

    context = {
        'video': video,
        'trends': trends,
        'advert': advert_content,
        'absolute_video_url': absolute_video_url,
        **common_context
    }

    return render(request, 'blog_details/video_details.html', context)