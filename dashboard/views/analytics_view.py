from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm, UserChangeForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth.tokens import default_token_generator
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from django.core.paginator import Paginator
from django.db.models import Q

from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.shortcuts import render, redirect


from django.shortcuts import render
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from blog.models import BlogPost, Category, User, Subscription
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta


from file_manager.models import File  # Import the File model from file_manager



def analytics_view(request):
    # Get today's date
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    start_of_month = today.replace(day=1)  # Start of the month

    # Posts count by date range
    posts_today = BlogPost.objects.filter(date__date=today).count()
    posts_this_week = BlogPost.objects.filter(date__gte=start_of_week).count()
    posts_this_month = BlogPost.objects.filter(date__gte=start_of_month).count()

    # Posts by category in date ranges
    categories_today = (
        BlogPost.objects.filter(date__date=today)
        .values('category__name')
        .annotate(count=Count('id'))
    )
    categories_this_week = (
        BlogPost.objects.filter(date__gte=start_of_week)
        .values('category__name')
        .annotate(count=Count('id'))
    )
    categories_this_month = (
        BlogPost.objects.filter(date__gte=start_of_month)
        .values('category__name')
        .annotate(count=Count('id'))
    )

    # Posts by user in date ranges
    posts_by_user_today = (
        BlogPost.objects.filter(date__date=today)
        .values('author__username')
        .annotate(count=Count('id'))
    )
    posts_by_user_this_week = (
        BlogPost.objects.filter(date__gte=start_of_week)
        .values('author__username')
        .annotate(count=Count('id'))
    )
    posts_by_user_this_month = (
        BlogPost.objects.filter(date__gte=start_of_month)
        .values('author__username')
        .annotate(count=Count('id'))
    )

    context = {
        'posts_today': posts_today,
        'posts_this_week': posts_this_week,
        'posts_this_month': posts_this_month,
        'categories_today': categories_today,
        'categories_this_week': categories_this_week,
        'categories_this_month': categories_this_month,
        'posts_by_user_today': posts_by_user_today,
        'posts_by_user_this_week': posts_by_user_this_week,
        'posts_by_user_this_month': posts_by_user_this_month,
    }

    return render(request, 'admin_home/analytics/analytics.html', context)