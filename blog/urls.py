# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),  # Use slug for the blog post
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'), 
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
