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


def reset_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Get users associated with the email
            users = form.get_users(email)

            # Send reset email to each user
            for user in users:
                context = {
                    'email': email,
                    'domain': request.get_host(),  
                    'site_name': 'Scodynate News',
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                }

                # Generate the plain text and HTML email content
                subject = render_to_string('registration/password-reset-email.txt', context).strip()
                plain_message = render_to_string('registration/password-reset-email.txt', context)  # Plain text version
                html_message = render_to_string('registration/password-reset-email.html', context)  # HTML version

                # Send email with both plain text and HTML content
                send_mail(
                    subject, 
                    plain_message,  # Plain text version
                    None, 
                    [email],
                    html_message=html_message,  # HTML version
                    fail_silently=False
                )

            return redirect(reverse_lazy('password_reset_done'))  # Redirect to the password reset done page

    else:
        form = PasswordResetForm()

    return render(request, 'registration/password-reset-form.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Check if both fields are filled
        if not username_or_email or not password:
            messages.error(request, mark_safe('<i class="fas fa-exclamation-circle"></i> Both fields are required.'))
            return render(request, 'registration/login.html')

        # Check if username or email exists in the database
        user = User.objects.filter(username=username_or_email).first() or User.objects.filter(email=username_or_email).first()

        if not user:
            messages.error(request, mark_safe('<i class="fas fa-user-times"></i> User does not exist. Please contact admin.'))
            return render(request, 'registration/login.html')

        # Authenticate the user
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, mark_safe('<i class="fas fa-check-circle"></i> Login successful!'))
                return redirect('dashboard_home')
            else:
                messages.error(request, mark_safe('<i class="fas fa-ban"></i> You do not have the required permissions to log in.'))
        else:
            messages.error(request, mark_safe('<i class="fas fa-key"></i> Invalid username or password.'))

    return render(request, 'registration/login.html')


# Staff and Superuser Logout View
@login_required
def user_logout(request):
    # If it's a POST request, log the user out
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('user_login')  # Redirect to the login page

    # Otherwise, show the confirmation page
    return render(request, 'registration/logout.html')