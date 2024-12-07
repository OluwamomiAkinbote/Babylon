from django.urls import path, include

from . import views

urlpatterns = [

    path('', views.dashboard_home, name='dashboard_home'),
    path('blog-table', views.blog_table, name='blog_table'),
    path('add-blog/', views.create_post, name='create_post'),
    path('edit-post/edit/<slug:slug>/', views.edit_blogpost, name='edit_blogpost'),
  
]
