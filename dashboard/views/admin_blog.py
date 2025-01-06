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
from file_manager.models import File



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
            # Fetch the category instance
            category = Category.objects.get(id=category_id)
         

            # Fetch the image from the file manager (if provided)
            image = None
            if image_id:
                image = File.objects.get(id=image_id)

            # Save the blog post, including the logged-in user as the author
            blog_post = BlogPost.objects.create(
                title=title,
                content=content,
                category=category,
                author=request.user,  # Set the author to the logged-in user
                image=image  # Assign the selected image (File instance)
            )


            return redirect('blog_table')  # Redirect to the blog table page after creating the post

        except Category.DoesNotExist:
            return render(request, 'admin_blog/create_post.html', {
                'categories': Category.objects.all(),
                'error': 'Selected category does not exist.'
            })

        except File.DoesNotExist:
            return render(request, 'admin_blog/create_post.html', {
                'categories': Category.objects.all(),
                'error': f'Selected image with ID {image_id} does not exist in the file manager.'
            })

        except Exception as e:
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

    # Fetch the blog post by slug
    blogpost = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        image_id = request.POST.get('image')  # Get the selected image ID (from file manager)

        try:


            # Update the blog post details
            blogpost.title = title
            blogpost.content = content

            # Update the category
            category = Category.objects.get(id=category_id)
            blogpost.category = category
           

            # Update the image if a new one is selected
            if image_id:
                image = File.objects.get(id=image_id)  # Fetch the image from the file manager
                blogpost.image = image  # Assign the new image
               

            # Save the changes
            blogpost.save()  
           

            # Redirect to the blog table page after editing the post
            return redirect('blog_table')  # Make sure this URL exists

        except Category.DoesNotExist:
            
            return render(request, 'admin_blog/edit_blog.html', {
                'blogpost': blogpost,
                'categories': Category.objects.all(),
                'error': 'Selected category does not exist.'
            })

        except File.DoesNotExist:
            
            return render(request, 'admin_blog/edit_blog.html', {
                'blogpost': blogpost,
                'categories': Category.objects.all(),
                'error': f'Selected image with ID {image_id} does not exist in the file manager.'
            })

        except Exception as e:
            # Catch all other exceptions for debugging
            print(f"Unexpected error: {e}")
            return render(request, 'admin_blog/edit_blog.html', {
                'blogpost': blogpost,
                'categories': Category.objects.all(),
                'error': 'An unexpected error occurred while updating the post.'
            })

    # Handle GET request: load the form with the blog post data and categories
    categories = Category.objects.all()
    return render(request, 'admin_blog/edit_blog.html', {
        'blogpost': blogpost,
        'categories': categories
    })





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