
from django.contrib import admin
from .models import BlogPost, Trend, Category, Media, Video, Subscription, AuthorProfile

from django.contrib import admin
from .models import AuthorProfile

@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'truncated_about', 'display_on_article', 'profile_picture')
    search_fields = ('user__username', 'user__email', 'about')
    list_filter = ('display_on_article',)
    ordering = ('user',)

    fieldsets = (
        (None, {
            'fields': ('user', 'profile_picture', 'about', 'display_on_article')
        }),
        ('Social Media Links', {
            'fields': ('twitter_url', 'facebook_url', 'linkedin_url', 'instagram_url', 'website_url'),
        }),
    )

    def truncated_about(self, obj):
        # Truncate the 'about' field to 30 characters for display in the list view
        return obj.about[:30] + '...' if obj.about and len(obj.about) > 30 else obj.about
    truncated_about.short_description = 'About'

    def save_model(self, request, obj, form, change):
        # Automatically set the user to the logged-in user if it's not set
        if not obj.user:
            obj.user = request.user

        super().save_model(request, obj, form, change)




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


# Register Trend model
@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')  # Added 'author'
    search_fields = ('title', 'content', 'author__username')  # Search by author's username
    ordering = ('-date',)
    fields = ('title', 'content', 'author', 'file', 'slug')  # Added 'author'
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
