# blog/admin.py
from django.contrib import admin
from .models import BlogPost, Category, Comment,  Media,Video
from .models import Subscription

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'show_on_navbar','priority')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('priority',)



@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category')
    search_fields = ('title', 'content')
    list_filter = ('date', 'category')
    ordering = ('-date',)
    fields = ('title', 'content', 'original_date', 'category', 'image', 'slug')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'file']
    search_fields = ['title']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'video_file', 'category')
    search_fields = ('title', 'description')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name','date_subscribed')  # Customize this to display the fields you want
    search_fields = ('email',)  # Add fields that you want to be searchable
    list_filter = ('date_subscribed',)  # Add fields to filter by

    # Optional: Add read-only fields if you don't want them to be editable in the admin
    readonly_fields = ('date_subscribed',)

class ReplyInline(admin.TabularInline):
    model = Comment
    fk_name = 'parent_comment'
    fields = ['author_name', 'text', 'date_posted']
    extra = 0  # Number of empty forms to display

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'date_posted', 'is_reply']
    list_filter = ['date_posted']
    search_fields = ['author_name', 'text']
    inlines = [ReplyInline]
