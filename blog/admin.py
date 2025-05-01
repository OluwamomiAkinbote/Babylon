from django.contrib import admin
from .models import BlogPost, Trend, Category, Subscription, AuthorProfile, Story, StoryMedia, BlogMedia
from datetime import timedelta

from django.utils.html import format_html

from django.utils.html import format_html
from django.contrib import admin
from django.contrib import admin
from .models import Story, StoryMedia

from django.contrib import admin
from django.utils.html import format_html
from filer.fields.file import FilerFileField
from .models import Story, StoryMedia
from datetime import timedelta

class StoryMediaInline(admin.TabularInline):
    model = StoryMedia
    extra = 1
    fields = ('media', 'caption', )  # Add a preview field


   

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'expires_at')  # Columns to show in the list view
    search_fields = ('title', 'user__username')  # Allow search by title and username
    ordering = ('-date',)  # Default ordering by date (descending)
    list_per_page = 20  # Pagination

    readonly_fields = ('date', 'expires_at')  # Prevent modification of date and expires_at

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'expires_at'),
        }),
        ('Timestamps', {
            'fields': ('date',),  # Only show the `date` field
        }),
    )

    inlines = [StoryMediaInline]

    def save_model(self, request, obj, form, change):
      
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

# Admin registrations for other models...from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'show_on_navbar', 'priority','slug' )
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('priority',)
    list_per_page = 20

    # This allows admins to filter by parent category
    list_filter = ('parent',)

    # Optionally add a hierarchical view for easier management of subcategories
    def parent_category(self, obj):
        return obj.parent.name if obj.parent else 'No Parent'
    parent_category.short_description = 'Parent Category'



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
    fields = ('title', 'lead', 'content', 'category', 'slug' )  
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20

    inlines = [BlogMediaInline] 



@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-date',)
    fields = ('title', 'content', 'author', 'file', 'slug', )
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)
    readonly_fields = ('date_subscribed',)
    list_per_page = 20
