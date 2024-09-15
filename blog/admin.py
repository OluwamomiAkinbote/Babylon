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
    list_display = ('title', 'date', 'category')
    search_fields = ('title', 'content')
    list_filter = ('date', 'category')
    ordering = ('-date',)
    fields = ('title', 'content',  'category', 'image', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title', 'content')
    ordering = ('-date',)
    fields = ('title', 'content', 'image', 'video', 'slug')
    prepopulated_fields = {'slug': ('title',)}

# Register Media model
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'file']
    search_fields = ['title']

# Register Video model
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_file', 'category','date')
    search_fields = ('title', 'description')

# Register Subscription model
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)
    readonly_fields = ('date_subscribed',)





