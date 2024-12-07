from django.contrib import admin
from .models import BlogPost, Trend, Category, Media, Video, Subscription


# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'show_on_navbar', 'priority')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('priority',)


# Register BlogPost model
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'category')  # Added 'author'
    search_fields = ('title', 'content', 'author__username')  # Search by author's username
    list_filter = ('date', 'category', 'author')  # Added 'author' to filters
    ordering = ('-date',)
    fields = ('title', 'content', 'author', 'category', 'image', 'slug')  # Added 'author'
    prepopulated_fields = {'slug': ('title',)}


# Register Trend model
@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')  # Added 'author'
    search_fields = ('title', 'content', 'author__username')  # Search by author's username
    ordering = ('-date',)
    fields = ('title', 'content', 'author', 'image', 'video', 'slug')  # Added 'author'
    prepopulated_fields = {'slug': ('title',)}


# Register Media model
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'file']
    search_fields = ['title']


# Register Video model
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'video_file', 'category', 'date')  # Added 'author'
    search_fields = ('title', 'description', 'author__username')  # Search by author's username
    list_filter = ('category', 'date', 'author')  # Added 'author' to filters
    ordering = ('-date',)
    fields = ('title', 'description', 'author', 'video_file', 'category', 'slug')  # Added 'author'


# Register Subscription model
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)
    readonly_fields = ('date_subscribed',)
