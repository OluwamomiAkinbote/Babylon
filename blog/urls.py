from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('more_stories/', views.more_stories, name='more_stories'),  # New path for "More Stories"
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]

