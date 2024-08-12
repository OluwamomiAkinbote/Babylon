from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')), 
    path("__reload__/", include("django_browser_reload.urls")),
    path('filer/', include('filer.urls')),
    path('tinymce/', include('tinymce.urls')),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
