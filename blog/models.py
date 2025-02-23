from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.templatetags.static import static
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site


class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')
    profile_picture = models.ImageField(upload_to='author_pics/', null=True, blank=True)
    about = models.TextField(max_length=1000, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    website_url = models.URLField(max_length=200, blank=True, null=True)
    display_on_article = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    show_on_navbar = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/category/{self.slug}/'


class BlogPost(models.Model):
    title = models.TextField(blank=True, null=True)
    content = HTMLField()
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name='blog_images')
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/blog/{self.slug}/'




class Trend(models.Model):
    title = models.TextField(blank=True, null=True)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name="trends")
    file = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL, related_name='trend_file')
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/trend/{self.slug}/'

    @property
    def is_image(self):
        return self.file and self.file.extension.lower() in ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'bmp', 'ico', 'tif', 'tiff', 'heic', 'heif', 'jfif', 'jpe', 'jif', 'jfi', 'jp2', 'j2k', 'jpf', 'jpx', 'jpm', 'mj2', 'j2c', 'jpc', 'j2', 'jpc', 'j2k', 'jpx', 'jpm', 'mj2', 'j2c', 'jpc', 'jif', 'jfif', 'jpe', 'jfi']

    @property
    def is_video(self):
        return self.file and self.file.extension.lower() == 'mp4'

    def get_file_url(self):
        """Return the absolute URL for the file."""
        if self.file:
            return self.file.url
        return None

    def get_absolute_file_url(self):
        """Returns the absolute URL with the current domain."""
        if self.file:
            return get_current_site(self.request).domain + self.file.url
        return None






class Video(models.Model):
    title = models.CharField(max_length=255)
    description = HTMLField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name="videos") 
    video_file = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL, related_name='video_files')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name='videos')
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/video/{self.slug}/'

    def get_thumbnail_url(self):
        """Return the thumbnail URL for the video or fallback to default."""
        if self.video_file:
            # Assuming we generate a thumbnail for the video using external service or local method
            return static('images/video-thumbnail.png')  # Replace with actual thumbnail generation logic
        return static('images/Breakingnews.png')  # Fallback image




class Subscription(models.Model):
    name = models.CharField(max_length=100, default='Anonymous')
    email = models.EmailField(unique=True, max_length=100)
    date_subscribed = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email
