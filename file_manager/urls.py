from django.urls import path
from . import views

urlpatterns = [
    path('', views.files_home, name='files_home'),
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('folder/<int:folder_id>/upload/', views.upload_file, name='upload_file'),
    path('folder/<int:folder_id>/edit/', views.edit_folder, name='edit_folder'),
    path('folder/<int:folder_id>/delete/', views.delete_folder, name='delete_folder'),  
    path('file_manager/folder/<int:parent_folder_id>/add/', views.add_folder, name='add_folder'),
    path('file_manager/folder/add/', views.add_folder, name='add_folder_no_parent'), 
    path('file/<int:file_id>/', views.file_details, name='file_details'),
]

