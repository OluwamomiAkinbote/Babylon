from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q
from blog.models import BlogPost, Category, Subscription
from advert.models import AdBanner
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from blog.models import BlogPost
from blog.serializers import BlogPostSerializer



def get_common_context():
    navbar_categories = Category.objects.filter(show_on_navbar=True).order_by('priority')
    leaderboard_ad = AdBanner.objects.filter(category='Leaderboard', active=True).first()
    sidebar_ad = AdBanner.objects.filter(category='Sidebar', active=True).first()
    home_ad = AdBanner.objects.filter(category='Home', active=True).first()

    return {
        'navbar_categories': navbar_categories,
        'leaderboard_ad': leaderboard_ad,
        'sidebar_ad': sidebar_ad,
        'home_ad': home_ad,
        'email': 'contact@scodynatenews.com',
        'current_time': datetime.now()
    }


def subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

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



@api_view(['GET'])
def search_api(request):
    query = request.GET.get('query', '')
    blogpost_results = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct().order_by('-date')

    paginator = PageNumberPagination()
    paginator.page_size = 9
    page = paginator.paginate_queryset(blogpost_results, request)
    serializer = BlogPostSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def suggestions_api(request):
    query = request.GET.get('query', '')
    suggestions = []

    if query:
        suggestions = list(
            BlogPost.objects.filter(title__icontains=query)
            .values_list('title', flat=True)
            .distinct()[:5]
        )
    
    return Response(suggestions)

