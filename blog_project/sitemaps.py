from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import BlogPost,  Category, Trend  # Assuming you have these models.

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'yearly'

    def items(self):
        return [
            'index',
            'privacy_policy',
            'data_deletion',
            'subscribe',
            'search_view',
            'video_reels',
            'trend_page',
            'get_suggestions',
            'more_stories',
        ]

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return BlogPost.objects.all()[:100]



class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Category.objects.all()

class TrendSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Trend.objects.all()

   
