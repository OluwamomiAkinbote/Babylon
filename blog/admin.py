from django.contrib import admin
from .models import BlogPost, Trend, Category, Video, Subscription, AuthorProfile


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'truncated_about', 'display_on_article', 'profile_picture')
    search_fields = ('user__username', 'user__email', 'about')
    list_filter = ('display_on_article',)
    ordering = ('user',)
    list_per_page = 20  # Pagination

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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'show_on_navbar', 'priority')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('priority',)
    list_per_page = 20  # Pagination


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category')
    search_fields = ('title', 'content')
    list_filter = ('date', 'category')
    ordering = ('-date',)
    fields = ('title', 'content', 'category', 'image', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20  # Pagination


@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-date',)
    fields = ('title', 'content', 'author', 'file', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20  # Pagination


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'video_file', 'category', 'date')
    search_fields = ('title', 'description', 'author__username')
    list_filter = ('category', 'date', 'author')
    ordering = ('-date',)
    fields = ('title', 'description', 'author', 'video_file', 'category', 'slug')
    list_per_page = 20  # Pagination


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)
    readonly_fields = ('date_subscribed',)
    list_per_page = 20  # Pagination
