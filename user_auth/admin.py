from django.contrib import admin
from .models import Interest, NewsUser, ComposeNews, Like, Retweet, Bookmark

# --- Interest Model Admin ---
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent', 'category', 'public_figure')
    search_fields = ('name', 'continent', 'category')
    list_filter = ('continent', 'category')

admin.site.register(Interest, InterestAdmin)

# --- NewsUser Model Admin ---
class NewsUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'bio')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('date_joined',)
    ordering = ('-date_joined',)

admin.site.register(NewsUser, NewsUserAdmin)

# --- ComposeNews Model Admin ---
class ComposeNewsAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'updated_at', 'is_reply')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at', 'is_reply')
    ordering = ('-created_at',)

admin.site.register(ComposeNews, ComposeNewsAdmin)

# --- Like Model Admin ---
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created_at')
    search_fields = ('user__username', 'news__content')
    list_filter = ('created_at',)

admin.site.register(Like, LikeAdmin)

# --- Retweet Model Admin ---
class RetweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'original_news', 'comment', 'created_at')
    search_fields = ('user__username', 'original_news__content', 'comment')
    list_filter = ('created_at',)

admin.site.register(Retweet, RetweetAdmin)

# --- Bookmark Model Admin ---
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created_at')
    search_fields = ('user__username', 'news__content')
    list_filter = ('created_at',)

admin.site.register(Bookmark, BookmarkAdmin)
