from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost, Category  
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from filer.models import File
from filer.fields.image import FilerImageField
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from filer.models.imagemodels import Image  
from django.core.files.base import ContentFile
from filer.models import Image
from django.core.paginator import Paginator

@login_required
def dashboard_home(request):
    if not request.user.is_staff:
        return redirect('blog_list')  
    return render(request, 'admin_home/home.html')






@login_required
def blog_table(request):
    if not request.user.is_staff:
        return redirect('dashboard_home')

    # Retrieve all blog posts, ordered by date
    blogposts = BlogPost.objects.all().order_by('-date')

    # Set up the paginator
    paginator = Paginator(blogposts, 20)  # Show 10 blog posts per page

    # Get the current page number from the request
    page_number = request.GET.get('page', 1)

    # Get the blog posts for the current page
    page_obj = paginator.get_page(page_number)

    # Pass the page object to the template
    return render(request, 'admin_blog/blog_table.html', {'page_obj': page_obj})






@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        uploaded_file = request.FILES.get('image')  # Get the uploaded file

        try:
            # Fetch the category instance
            category = Category.objects.get(id=category_id)

            # Create a Filer Image instance if an image is uploaded
            filer_image = None
            if uploaded_file:
                filer_image = Image.objects.create(
                    owner=request.user,  # Optional: set the owner to the logged-in user
                    original_filename=uploaded_file.name,
                    file=uploaded_file
                )

            # Save the blog post
            BlogPost.objects.create(
                title=title,
                content=content,
                category=category,
                image=filer_image  # Assign the Filer Image instance
            )
            return redirect('blog_table')  # Replace with your desired redirect

        except Category.DoesNotExist:
            return render(request, 'admin_blog/create_post.html', {
                'categories': Category.objects.all(),
                'error': 'Selected category does not exist.'
            })

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




from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Permission

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











