from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.contrib.auth.models import User


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


class Media(models.Model):
    title = models.CharField(max_length=255)
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name='media_images')
    file = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL, related_name='media_files')

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.TextField(blank=True, null=True)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="blogposts")
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = FilerImageField(null=True, blank=True, related_name="blog_images", on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Trend(models.Model):
    title = models.TextField(blank=True, null=True)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name="trends") 
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name='trend_image')
    video = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL, related_name='trend_video')
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = HTMLField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name="videos") 
    video_file = FilerFileField(null=True, blank=True, related_name="video_files", on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name='videos')
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    name = models.CharField(max_length=100, default='Anonymous')
    email = models.EmailField(unique=True, max_length=100)
    date_subscribed = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email
