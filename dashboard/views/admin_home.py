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














# Dashboard Home View
@login_required
def dashboard_home(request):
    # Ensure the user is staff before accessing the dashboard
    if not request.user.is_staff:
        return redirect('index')  # If the user is not staff, redirect to the index

    # Render the dashboard home page
    response = render(request, 'admin_home/home.html')
    # Set a cookie for demonstration
    response.set_cookie('my_cookie', 'cookie_value', max_age=3600)  # Expires in 1 hour

    return response
