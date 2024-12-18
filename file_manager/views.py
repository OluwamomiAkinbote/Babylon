from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Folder, File
from .utils import detect_file_type

def files_home(request):
    # Query for root folders (folders with no parent)
    folders = Folder.objects.filter(parent_folder__isnull=True).order_by('-date')
    return render(request, 'file_manager/files_home.html', {'folders': folders})



def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    files = folder.files.all().order_by('-date')  # Directly retrieve files in the folder

    # Add additional file metadata for display
    for file in files:
        file.extension = file.file.url.split('.')[-1].lower()
        file.file_type = detect_file_type(file.file.url)

    return render(request, 'file_manager/folder_details.html', {
        'folder': folder,
        'files': files,  # Only files are passed
    })



def upload_file(request, folder_id):
    # Retrieve the folder by ID or return 404
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Check if a file with the same name already exists in the folder
        if folder.files.filter(name=uploaded_file.name).exists():
            messages.error(request, f"A file named '{uploaded_file.name}' already exists in this folder.")
        else:
            # Create the file object and associate it with the folder
            File.objects.create(folder=folder, file=uploaded_file, name=uploaded_file.name)
            messages.success(request, "File uploaded successfully.")
        
        return redirect('folder_detail', folder_id=folder.id)

    return render(request, 'file_manager/upload_file.html', {'folder': folder})



def add_folder(request, parent_folder_id=None):
    parent_folder = get_object_or_404(Folder, id=parent_folder_id) if parent_folder_id else None

    if request.method == 'POST':
        folder_name = request.POST.get('name')
        if not folder_name:
            messages.error(request, "Folder name cannot be empty.")
        elif parent_folder and parent_folder.subfolders.filter(name=folder_name).exists():
            messages.error(request, f"A subfolder named '{folder_name}' already exists.")
        else:
            Folder.objects.create(name=folder_name, parent_folder=parent_folder)
            messages.success(request, "Folder created successfully.")
            return redirect('folder_detail', folder_id=parent_folder.id) if parent_folder else redirect('files_home')

    return render(request, 'file_manager/add_folder.html', {'parent_folder': parent_folder})


def edit_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        folder_name = request.POST.get('name')
        if not folder_name:
            messages.error(request, "Folder name cannot be empty.")
        elif folder.parent_folder and folder.parent_folder.subfolders.filter(name=folder_name).exclude(id=folder.id).exists():
            messages.error(request, f"A folder named '{folder_name}' already exists in the parent folder.")
        else:
            folder.name = folder_name
            folder.save()
            messages.success(request, "Folder updated successfully.")
            return redirect('folder_detail', folder_id=folder.id)

    return render(request, 'file_manager/edit_folder.html', {'folder': folder})


def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        parent_folder_id = folder.parent_folder.id if folder.parent_folder else None
        folder.delete()
        messages.success(request, f"Folder '{folder.name}' deleted successfully.")
        return redirect('folder_detail', folder_id=parent_folder_id) if parent_folder_id else redirect('files_home')

    return render(request, 'file_manager/delete_confirmation.html', {'folder': folder})


def file_details(request, file_id):
    file = get_object_or_404(File, id=file_id)

    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name and not file.folder.files.filter(name=new_name).exclude(id=file.id).exists():
            file.name = new_name
            file.save()
            messages.success(request, "File name updated successfully.")
        else:
            messages.error(request, f"A file named '{new_name}' already exists in this folder.")
        return redirect('folder_detail', folder_id=file.folder.id)

    file.extension = file.file.url.split('.')[-1].lower()
    file.file_type = detect_file_type(file.file.url)

    return render(request, 'file_manager/file_details.html', {'file': file})


def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    folder_id = file.folder.id

    if request.method == 'POST':
        file.delete()
        messages.success(request, f"File '{file.name}' deleted successfully.")
        return redirect('folder_detail', folder_id=folder_id)

    return render(request, 'file_manager/delete_confirmation.html', {'file': file})
