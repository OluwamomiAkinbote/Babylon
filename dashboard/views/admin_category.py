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



# View to list all users
def user_table(request):
    users = User.objects.all()
    return render(request, 'admin_users/user_table.html', {'users': users})

# View to edit user details (and permissions)
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'admin_users/edit_user.html', {'form': form, 'user': user})


# category model

def category_table(request):
    categories = Category.objects.all().order_by('priority')
    return render(request, 'admin_category/admin_category.html', {'categories': categories})

def create_category(request):
    if request.method == "POST":
        name = request.POST.get('name')
        show_on_navbar = request.POST.get('show_on_navbar') == 'on'
        priority = request.POST.get('priority', 0)

        category = Category(name=name, show_on_navbar=show_on_navbar, priority=priority)
        category.save()
        return redirect(reverse('category_table'))

    return render(request, 'admin_category/create_category.html')

def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        category.name = request.POST.get('name')
        category.show_on_navbar = request.POST.get('show_on_navbar') == 'on'
        category.priority = request.POST.get('priority', 0)
        category.save()
        return redirect(reverse('category_table'))

    return render(request, 'admin_category/edit_category.html', {'category': category})

def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        category.delete()
        return redirect(reverse('category_table'))
    return render(request, 'admin_category/delete_category.html', {'category': category})














