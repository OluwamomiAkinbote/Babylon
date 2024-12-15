from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class File(models.Model):
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='file_manager/')
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    
