from django.db import models
import mimetypes
import os



def upload_to(instance, filename):
    """Dynamic upload path based on the folder structure."""
    folder_name = instance.folder.name if instance.folder else "default"
    return f"file_manager/{folder_name}/{filename}"

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subfolders'
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Folders"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Parent: {self.parent_folder.name if self.parent_folder else 'Root'})"

    def get_immediate_files(self):
        """Retrieve only the immediate files in this folder."""
        return self.files.all()

    def get_immediate_subfolders(self):
        """Retrieve only the immediate subfolders in this folder."""
        return self.subfolders.all()

    def calculate_size(self):
        """Calculate the total size of all immediate files in this folder."""
        return sum(file.file.size for file in self.files.all())

class File(models.Model):
    folder = models.ForeignKey(
        Folder,
        related_name='files',
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to=upload_to)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Files"
        ordering = ['name']
        unique_together = ('folder', 'name')  # Ensure unique file names within a folder

    def __str__(self):
        return self.name

    def get_file_type(self):
        """
        Determine the type of file based on MIME type.
        Returns "image", "video", "audio", "text", "application", or "unknown".
        """
        mime_type, _ = mimetypes.guess_type(self.file.name)
        if mime_type:
            return mime_type.split('/')[0]  # Extract the category from the MIME type
        return "unknown"

    def is_image(self):
        """Check if the file is an image."""
        return self.get_file_type() == "image"

    def is_video(self):
        """Check if the file is a video."""
        return self.get_file_type() == "video"

    def is_audio(self):
        """Check if the file is an audio file."""
        return self.get_file_type() == "audio"

    def extension(self):
        """Get the file extension."""
        return os.path.splitext(self.file.name)[1].lower()

    def size_in_mb(self):
        """Get the file size in MB, rounded to 2 decimal places."""
        return round(self.file.size / (1024 * 1024), 2)
