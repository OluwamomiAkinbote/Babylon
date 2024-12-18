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




@login_required
def blog_table(request):
    if not request.user.is_staff:
        return redirect('dashboard_home')

    blogposts = BlogPost.objects.all().order_by('-date')
    paginator = Paginator(blogposts, 20)  

    page_number = request.GET.get('page', 1)

    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_blog/blog_table.html', {'page_obj': page_obj})




@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        image_id = request.POST.get('image')  # Get the selected image ID (from file manager)

        try:
            # Debug: Log the received data
            print(f"Received data: title={title}, content={content}, category_id={category_id}, image_id={image_id}")

            # Fetch the category instance
            category = Category.objects.get(id=category_id)
            print(f"Category fetched: {category}")

            # Fetch the image from the file manager (if provided)
            image = None
            if image_id:
                image = File.objects.get(id=image_id)
                print(f"Image fetched: {image}")

            # Save the blog post, including the logged-in user as the author
            blog_post = BlogPost.objects.create(
                title=title,
                content=content,
                category=category,
                author=request.user,  # Set the author to the logged-in user
                image=image  # Assign the selected image (File instance)
            )
            print(f"Blog post created successfully: {blog_post}")

            return redirect('blog_table')  # Redirect to the blog table page after creating the post

        except Category.DoesNotExist:
            print(f"Category with ID {category_id} does not exist.")
            return render(request, 'admin_blog/create_post.html', {
                'categories': Category.objects.all(),
                'error': 'Selected category does not exist.'
            })

        except File.DoesNotExist:
            print(f"File with ID {image_id} does not exist.")
            return render(request, 'admin_blog/create_post.html', {
                'categories': Category.objects.all(),
                'error': f'Selected image with ID {image_id} does not exist in the file manager.'
            })

        except Exception as e:
            # Catch all other exceptions for debugging
            print(f"Unexpected error: {e}")
            return render(request, 'admin_blog/create_post.html', {
                'categories': Category.objects.all(),
                'error': 'An unexpected error occurred while creating the post.'
            })

    # Handle GET request: load the form with existing categories
    categories = Category.objects.all()
    return render(request, 'admin_blog/create_post.html', {'categories': categories})






@login_required
def edit_blogpost(request, slug):
    if not request.user.is_staff:
        return redirect('dashboard_home')

    blogpost = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        blogpost.title = request.POST['title']
        blogpost.content = request.POST['content']
        blogpost.category_id = request.POST['category']

        # Check if a new image is uploaded
        if 'image' in request.FILES:
            if blogpost.image:  # Check if the blogpost already has an image
                blogpost.image.delete()  # Delete the old image if it exists

            # Create a new FilerImage instance using the uploaded file
            image_file = request.FILES['image']
            image_instance = Image.objects.create(file=image_file)  # Save image file to the FilerImage model
            blogpost.image = image_instance  # Assign it to the BlogPost image field

        blogpost.save()
        return redirect('blog_table')

    categories = Category.objects.all()
    return render(request, 'admin_blog/edit_blog.html', {'blogpost': blogpost, 'categories': categories})




@login_required
def delete_blogpost(request, slug):
    if not request.user.is_staff:
        return redirect('dashboard_home')

    blogpost = get_object_or_404(BlogPost, slug=slug)
    
    if request.method == "POST":
        blogpost.delete()
        return redirect('blog_table')
    
    # Render a confirmation template
    return render(request, 'admin_blog/delete_blog.html', {'blogpost': blogpost})




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






