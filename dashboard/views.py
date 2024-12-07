from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost, Category  
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from filer.models import File
from filer.fields.image import FilerImageField

@login_required
def dashboard_home(request):
    if not request.user.is_staff:
        return redirect('blog_list')  
    return render(request, 'admin_home/home.html')



@login_required
def blog_table(request):
    if not request.user.is_staff:
        return redirect('dashboard_home')
    blogposts = BlogPost.objects.all().order_by('-date')
    return render(request, 'admin_blog/blog_table.html', {'blogposts': blogposts})



@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        # Fetch the category instance
        category = Category.objects.get(id=category_id)

        # Save the blog post
        BlogPost.objects.create(
            title=title,
            content=content,
            category=category,
            image=image
        )
        return redirect('blog_table')  # Replace with your desired redirect

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
        blogpost.save()
        return redirect('blog_table')
    categories = Category.objects.all()
    return render(request, 'admin_blog/edit_blog.html', {'blogpost': blogpost, 'categories': categories})







"""






@login_required
def manage_blogposts(request):
    if not request.user.is_staff:
        return redirect('dashboard_home')
    blogposts = BlogPost.objects.all()
    return render(request, 'dashboard/blogposts.html', {'blogposts': blogposts})

@login_required
def add_blogpost(request):
    if not request.user.is_staff:
        return redirect('dashboard_home')
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']
        BlogPost.objects.create(
            title=title,
            content=content,
            category_id=category_id
        )
        return redirect('manage_blogposts')
    categories = Category.objects.all()
    return render(request, 'dashboard/add_blogpost.html', {'categories': categories})

@login_required
def edit_blogpost(request, id):
    if not request.user.is_staff:
        return redirect('dashboard_home')
    blogpost = get_object_or_404(BlogPost, id=id)
    if request.method == 'POST':
        blogpost.title = request.POST['title']
        blogpost.content = request.POST['content']
        blogpost.category_id = request.POST['category']
        blogpost.save()
        return redirect('manage_blogposts')
    categories = Category.objects.all()
    return render(request, 'dashboard/edit_blogpost.html', {'blogpost': blogpost, 'categories': categories})

@login_required
def delete_blogpost(request, id):
    if not request.user.is_staff:
        return redirect('dashboard_home')
    blogpost = get_object_or_404(BlogPost, id=id)
    blogpost.delete()
    return redirect('manage_blogposts')

"""