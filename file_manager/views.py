from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Folder, File
from mimetypes import guess_type


# Home view to list all folders
def files_home(request):
    # Get all folders in the file manager
    folders = Folder.objects.all()
    return render(request, 'file_manager/files_home.html', {'folders': folders})


# Folder detail view to show files within a specific folder
def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    files = File.objects.filter(folder=folder)

    # Define file type categories
    image_extensions = ['jpg', 'jpeg', 'png', 'gif']
    video_extensions = ['mp4', 'avi', 'mov', 'webm', 'mkv']
    pdf_extensions = ['pdf']
    document_extensions = ['docx', 'doc', 'xlsx', 'xls', 'pptx', 'txt']

    # Add `extension` and `file_type` attributes to each file
    for file in files:
        file.extension = file.file.url.split('.')[-1].lower()  # Extract and normalize file extension
        mime_type, _ = guess_type(file.file.url)
        file.file_type = 'image' if file.extension in image_extensions else (
            'video' if file.extension in video_extensions else (
                'pdf' if file.extension in pdf_extensions else (
                    'document' if file.extension in document_extensions else 'unsupported'
                )
            )
        )

    return render(request, 'file_manager/folder_details.html', {
        'folder': folder,
        'files': files,
        'image_extensions': image_extensions,
        'video_extensions': video_extensions,
    })


# File upload view to handle uploading files to a specific folder
def upload_file(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Determine file type (image or video based on file extension)
        file_type = 'image' if uploaded_file.name.lower().endswith(('jpg', 'jpeg', 'png')) else 'video'

        # Create a new File object for the uploaded file
        new_file = File.objects.create(
            folder=folder,
            file=uploaded_file,
            name=uploaded_file.name,
        )

        # Redirect to folder detail page after successful file upload
        return redirect('folder_detail', folder_id=folder.id)

    # Return upload file form page if request method is GET
    return render(request, 'file_manager/upload_file.html', {'folder': folder})


# File rename view to rename an existing file
def rename_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        file.name = new_name
        file.save()

        # Redirect to the folder detail page after renaming
        return redirect('folder_detail', folder_id=file.folder.id)

    # Render the rename file form
    return render(request, 'file_manager/rename_file.html', {'file': file})


# Add folder view to create a new folder
def add_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('name')

        # Ensure folder name is provided
        if not folder_name:
            messages.error(request, "Folder name cannot be empty.")
            return redirect('add_folder')

        # Create new folder
        new_folder = Folder.objects.create(name=folder_name)

        # Redirect to home or folder details after creating
        return redirect('files_home')  # or redirect('folder_detail', folder_id=new_folder.id)

    # Render add folder form
    return render(request, 'file_manager/add_folder.html')


# Edit folder view to update an existing folder's details
def edit_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if request.method == 'POST':
        folder_name = request.POST.get('name')

        # Ensure folder name is provided
        if not folder_name:
            messages.error(request, "Folder name cannot be empty.")
            return redirect('edit_folder', folder_id=folder.id)

        folder.name = folder_name
        folder.save()

        # Redirect to folder detail page after updating
        return redirect('files_home')

    # Render edit folder form
    return render(request, 'file_manager/edit_folder.html', {'folder': folder})


# Folder delete view to confirm and delete folder
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    
    if request.method == 'POST':
        # Delete the folder if the request is POST
        folder.delete()
        messages.success(request, f"Folder '{folder.name}' has been deleted successfully.")
        return redirect('files_home')

    # If the request is GET, show the confirmation page
    return render(request, 'file_manager/delete_confirmation.html', {'folder': folder})
