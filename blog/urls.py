# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'), 
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('subscribe/', views.subscribe, name='subscribe'),
   
]

