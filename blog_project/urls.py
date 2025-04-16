from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from blog_project.sitemaps import StaticViewSitemap, BlogSitemap,  CategorySitemap, TrendSitemap
from django.views.generic.base import TemplateView

sitemaps = {
    'static': StaticViewSitemap,
    'blogs': BlogSitemap,
    'categories': CategorySitemap,
    'trends': TrendSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('news-admin/', admin.site.urls),
    path('', include('blog.urls')), 
    path('advert/', include('advert.urls')), 
    path('shop/', include('shop.urls')), 
    path('dashboard/', include('dashboard.urls')), 
    path('file_manager/', include('file_manager.urls')), 
    path("__reload__/", include("django_browser_reload.urls")),
    path('filer/', include('filer.urls')),
    path('tinymce/', include('tinymce.urls')),
    
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
