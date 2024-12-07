from django.urls import path, include

from . import views

urlpatterns = [

    path('', views.dashboard_home, name='dashboard_home'),
    path('blog-table', views.blog_table, name='blog_table'),
    path('add-blog/', views.create_post, name='create_post'),
    path('admin-users/', views.user_table, name='user_table'),
    path('edit-post/edit/<slug:slug>/', views.edit_blogpost, name='edit_blogpost'),
    path('blogpost/<slug:slug>/delete/', views.delete_blogpost, name='delete_blogpost'),
  
]
