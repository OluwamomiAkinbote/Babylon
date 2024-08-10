# models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    show_on_navbar = models.BooleanField(default=False)  # New field to control navbar display
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
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_file = FilerFileField(null=True, blank=True, related_name="video_files", on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name='videos')

    def save(self, *args, **kwargs):
        if not self.category:
            video_category, created = Category.objects.get_or_create(name='Videos')
            self.category = video_category
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class BlogPost(models.Model):
    title = models.CharField(max_length=500, unique=True)
    content = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    original_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = FilerImageField(null=True, blank=True, related_name="blog_images", on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField(blank=True, null=True)
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    likes_count = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def toggle_like(self, user):
        if self.liked_by.filter(id=user.id).exists():
            self.liked_by.remove(user)
            self.likes_count -= 1
        else:
            self.liked_by.add(user)
            self.likes_count += 1
        self.save()

    def __str__(self):
        return f'Comment by {self.author_name} on {self.post}'

    def is_reply(self):
        return self.parent_comment is not None


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


