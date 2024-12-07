from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('search/', views.search_view, name='search_view'),
    path('video_reels', views.video_reels, name='video_reels'),
    path('trend_page', views.trend_page, name='trend_page'),
    path('get-suggestions/', views.get_suggestions, name='get_suggestions'),
    path('more_stories/', views.more_stories, name='more_stories'),  
    path('trend/<slug:slug>/', views.trend_detail, name='trend_detail'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('videos/<slug:slug>/', views.video_detail, name='video_details'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

]
