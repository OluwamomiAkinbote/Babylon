from django.db import models
import mimetypes

def upload_to(instance, filename):
    """Dynamic upload path based on the folder structure."""
    return f"file_manager/{instance.folder.name}/{filename}"

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
        """Calculate the total size of immediate files in this folder."""
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
        """Determine the type of file."""
        mime_type, _ = mimetypes.guess_type(self.file.name)
        if mime_type:
            return mime_type.split('/')[0]  # e.g., "image", "video", "application"
        return "unknown"
