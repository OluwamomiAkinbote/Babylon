from django.contrib import admin
from .models import Folder, File

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'date')
    search_fields = ['name']

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_folder', 'date')
    search_fields = ['name']

admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)

