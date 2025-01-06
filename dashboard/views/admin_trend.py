from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Trend
from file_manager.models import File
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.shortcuts import render

def trend_table(request):
    trends = Trend.objects.all().order_by('-date')
    paginator = Paginator(trends, 20)  # Show 10 trends per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the trends for the current page
    return render(request, 'admin_blog/trends/trend_table.html', {'page_obj': page_obj})


@login_required
def create_trend(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        file_id = request.POST.get('file_id')  # ID of the selected file from the file manager

        # Validate title and content
        if not title or not content:
            messages.error(request, 'Title and content are required.')
            return redirect('create_trend')

        # Handle file selection
        file = None
        if file_id:
            try:
                file = File.objects.get(id=file_id)
            except File.DoesNotExist:
                messages.error(request, 'Invalid file selection.')
                return redirect('create_trend')

        # Create the Trend
        trend = Trend(
            title=title,
            content=content,
            author=request.user,
            file=file,  # Assign the selected file
            slug=slugify(title)
        )
        trend.save()

        messages.success(request, 'Trend created successfully!')
        return redirect('trend_table')

    return render(request, 'admin_blog/trends/create_trend.html')

# View for editing an existing trend
@login_required
def edit_trend(request, slug):
    trend = get_object_or_404(Trend, slug=slug)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        file_id = request.POST.get('file_id')  # ID of the new selected file

        # Validate title and content
        if not title or not content:
            messages.error(request, 'Title and content are required.')
            return redirect('edit_trend', slug=slug)

        # Update the trend fields
        trend.title = title
        trend.content = content
        trend.slug = slugify(title)

        # Handle file update
        if file_id:
            try:
                trend.file = File.objects.get(id=file_id)
            except File.DoesNotExist:
                messages.error(request, 'Invalid file selection.')
                return redirect('edit_trend', slug=slug)

        trend.save()
        messages.success(request, 'Trend updated successfully!')
        return redirect('trend_table')

    return render(request, 'admin_blog/trends/edit_trend.html', {'trend': trend})

# View for deleting a trend
@login_required
def delete_trend(request, slug):
    trend = get_object_or_404(Trend, slug=slug)
    if request.method == 'POST':
        trend.delete()
        messages.success(request, 'Trend deleted successfully!')
        return redirect('trend_table')
    return render(request, 'admin_blog/trends/delete_trend.html', {'trend': trend})
