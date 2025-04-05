from django.contrib import admin
from .models import BlogPost, Trend, Category, Video, Subscription, AuthorProfile, Story, StoryMedia, BlogMedia
from datetime import timedelta

from django.utils.html import format_html

from django.utils.html import format_html
from django.contrib import admin
from django.contrib import admin
from .models import Story, StoryMedia

class StoryMediaInline(admin.TabularInline):
    model = StoryMedia
    extra = 1
    fields = ('media', 'caption', 'preview')  # Add a preview field
    readonly_fields = ('preview',)  # Make the preview field non-editable

    def preview(self, obj):
        if obj.media:
            if obj.media.url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                return format_html(f'<img src="{obj.media.url}" width="100" height="100" style="object-fit: cover;"/>')
            elif obj.media.url.endswith(('.mp4', '.webm', '.ogg')):
                return format_html(f'<video width="100" height="100" controls><source src="{obj.media.url}" type="video/mp4">Your browser does not support the video tag.</video>')
        return "No media"

    preview.short_description = "Preview"

    class Media:
        js = ('admin/js/vendor/jquery/jquery.js', 'admin/js/actions.js', 'js/preview_update.js')  

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'expires_at')  # Columns to show in the list view
    search_fields = ('title', 'user__username')  # Allow search by title and username
    ordering = ('-date',)  # Default ordering by date (descending)
    list_per_page = 20  # Pagination

    readonly_fields = ('date','expires_at')  # Prevent modification of date

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'expires_at'),  # Remove created_at from here
        }),
        ('Timestamps', {
            'fields': ('date',),  # Place it in its own section as read-only
        }),
    )

    inlines = [StoryMediaInline]


    def save_model(self, request, obj, form, change):
        if not obj.expires_at:
            obj.expires_at = obj.created_at + timedelta(days=3)  # Default expiration is 3 days from creation
        super().save_model(request, obj, form, change)

# Other existing admin registrations (as per your previous code)
@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'truncated_about', 'display_on_article', 'profile_picture')
    search_fields = ('user__username', 'user__email', 'about')
    list_filter = ('display_on_article',)
    ordering = ('user',)
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('user', 'profile_picture', 'about', 'display_on_article')
        }),
        ('Social Media Links', {
            'fields': ('twitter_url', 'facebook_url', 'linkedin_url', 'instagram_url', 'website_url'),
        }),
    )

    def truncated_about(self, obj):
        return obj.about[:30] + '...' if obj.about and len(obj.about) > 30 else obj.about
    truncated_about.short_description = 'About'

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

# Admin registrations for other models...
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'show_on_navbar', 'priority')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('priority',)
    list_per_page = 20

class BlogMediaInline(admin.TabularInline):
    model = BlogMedia
    extra = 1  # Allows adding multiple media files
    fields = ('media', 'caption')  # Only show the media upload field

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category')
    search_fields = ('title', 'content')
    list_filter = ('date', 'category')
    ordering = ('-date',)
    fields = ('title', 'content', 'category', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20

    inlines = [BlogMediaInline]  # ← This line adds BlogMedia as inline


@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-date',)
    fields = ('title', 'content', 'author', 'file', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'video_file', 'category', 'date')
    search_fields = ('title', 'description', 'author__username')
    list_filter = ('category', 'date', 'author')
    ordering = ('-date',)
    fields = ('title', 'description', 'author', 'video_file', 'category', 'slug')
    list_per_page = 20

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)
    readonly_fields = ('date_subscribed',)
    list_per_page = 20
