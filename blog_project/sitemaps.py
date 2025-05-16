from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import BlogPost, Category, Trend  # Assuming you have these models.


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'yearly'

    def items(self):
        return [
            'home',
            'privacy_policy',
            'data_deletion',
            'subscribe',
            'search_view',
            'trend_page',
            'get_suggestions',
            'more_stories',
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.9

    def items(self):
        # Order by newest date first, limit to 100 latest posts
        return BlogPost.objects.order_by('-date')[:100]

    def lastmod(self, obj):
        # Return the publish date for sitemap lastmod
        return obj.date


class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Category.objects.all()


class TrendSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Trend.objects.order_by('-date')[:100]
    
    def lastmod(self, obj):
        # Return the publish date for sitemap lastmod
        return obj.date
  
