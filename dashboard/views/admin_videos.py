from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from blog.models import Video, Category
from file_manager.models import File

# List all videos with pagination
def video_table(request):
    videos_list = Video.objects.all()

    paginator = Paginator(videos_list, 20)  # Show 20 videos per page
    page_number = request.GET.get('page')  # Get the page number from the URL query string
    page_obj = paginator.get_page(page_number)  # Get the page object

    return render(request, 'admin_blog/videos/video_table.html', {'page_obj': page_obj})






def create_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        video_file_id = request.POST.get('video_file')  # Get the selected video file ID (if using a file manager)

        try:
            # Fetch the category instance
            category = Category.objects.get(id=category_id)

            # Fetch the video file from the file manager (if provided)
            video_file = None
            if video_file_id:
                video_file = File.objects.get(id=video_file_id)

            # Save the video, including the logged-in user as the author
            video = Video.objects.create(
                title=title,
                description=description,
                category=category,
                author=request.user,  # Set the author to the logged-in user
                video_file=video_file  # Assign the selected video file (File instance)
            )

            return redirect('video_table')  # Redirect to the video list page after creating the video

        except Category.DoesNotExist:
            return render(request, 'admin_blog/videos/create_video.html', {
                'categories': Category.objects.all(),
                'error': 'Selected category does not exist.'
            })

        except File.DoesNotExist:
            return render(request, 'admin_blog/videos/create_video.html', {
                'categories': Category.objects.all(),
                'error': f'Selected video file with ID {video_file_id} does not exist in the file manager.'
            })

        except Exception as e:
            return render(request, 'admin_blog/videos/create_video.html', {
                'categories': Category.objects.all(),
                'error': 'An unexpected error occurred while creating the video.'
            })

    # Handle GET request: load the form with existing categories
    categories = Category.objects.all()
    return render(request, 'admin_blog/videos/create_video.html', {'categories': categories})




def edit_video(request, slug):
    video = get_object_or_404(Video, slug=slug)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        video_file_id = request.POST.get('video_file')  # Get the video file ID (if provided)
        
        try:
            # Update the title and description
            video.title = title
            video.description = description
            
            # Update the category
            category = Category.objects.get(id=category_id)
            video.category = category
            
            # Update the video file if a new one is provided
            if video_file_id:
                video_file = File.objects.get(id=video_file_id)
                video.video_file = video_file  # Assign the new video file (File instance)
            elif request.FILES.get('video_file'):
                # Handle file upload if a file is uploaded via the form
                video.video_file = request.FILES.get('video_file')

            # Save the video
            video.save()

            
            return redirect('video_table')

        except Category.DoesNotExist:
            return render(request, 'admin_blog/videos/edit_video.html', {
                'video': video,
                'categories': Category.objects.all(),
                'error': 'Selected category does not exist.'
            })

        except File.DoesNotExist:
            return render(request, 'admin_blog/videos/edit_video.html', {
                'video': video,
                'categories': Category.objects.all(),
                'error': 'Selected video file does not exist in the file manager.'
            })

        except Exception as e:
            return render(request, 'admin_blog/videos/edit_video.html', {
                'video': video,
                'categories': Category.objects.all(),
                'error': 'An unexpected error occurred while updating the video.'
            })
    
    # Handle GET request: load the form with existing video details and categories
    categories = Category.objects.all()
    return render(request, 'admin_blog/videos/edit_video.html', {
        'video': video,
        'categories': categories
    })





# Delete a video
def delete_video(request, slug):
    video = get_object_or_404(Video, slug=slug)
    if request.method == 'POST':
        video.delete()
        return redirect('video_table')
    return render(request, 'admin_blog/videos/delete_video.html', {'video': video})
