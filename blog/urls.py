from django.urls import path
from . import views
from .views import IndexAPIView,MainExclusiveAPIView, NewsListView, BlogDetailAPIView, TrendDetailAPIView, FeaturedCategoryPostsView
from .views import MoreStoriesAPIView, TrendPageAPIView
from .views import PrivacyPolicyAPIView, DataDeletionAPIView, CategoryListAPIView, HeroPostsAPIView
from .views import GlobalNewsAPIView, SportsTechAPIView, TrendAPIView
from .views import StoryListCreateAPIView, StoryDetailAPIView, StoryMediaListCreateAPIView, StoryMediaDetailAPIView, HeaderAPIView



urlpatterns = [
    path('', IndexAPIView.as_view(), name='home'),
    path('header', HeaderAPIView.as_view(), name='header'),
    path("hero-posts/", HeroPostsAPIView.as_view(), name="hero-posts"),
    path("main-exclusive/", MainExclusiveAPIView.as_view(), name="main-exclusive"),
    path("global-news/",GlobalNewsAPIView.as_view(), name="global-news"),
    path("sports-tech/", SportsTechAPIView.as_view(), name="sports-tech"),
    path("featured-categories/", FeaturedCategoryPostsView.as_view(), name="featured-categories"),
    path("trends/", TrendAPIView.as_view(), name="trends"),
    path('story/', StoryListCreateAPIView.as_view(), name='story-list-create'),
    path('story/<int:pk>/', StoryDetailAPIView.as_view(), name='story-detail'),
    path('story-media/', StoryMediaListCreateAPIView.as_view(), name='story-media-list-create'),
    path('story-media/<int:pk>/', StoryMediaDetailAPIView.as_view(), name='story-media-detail'),

    path('privacy-policy/', PrivacyPolicyAPIView.as_view(), name='privacy_policy'),
    path('data-deletion/', DataDeletionAPIView.as_view(), name='data_deletion'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('search/', views.search_view, name='search_view'),

    path('trend_page', TrendPageAPIView.as_view(), name='trend_page'),
    path('get-suggestions/', views.get_suggestions, name='get_suggestions'),
    path('more_stories/', MoreStoriesAPIView.as_view(), name='more_stories'),  
    path('trend/<slug:slug>/', TrendDetailAPIView.as_view(), name='trend_detail'),
    path('category/<slug:slug>/', CategoryListAPIView.as_view(), name='category_list'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', BlogDetailAPIView.as_view(), name='blog_detail'),

]
