from django.contrib import admin
from .models import Interest, Member

# --- Interest Model Admin ---
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent', 'category', 'public_figure')
    search_fields = ('name', 'continent', 'category')
    list_filter = ('continent', 'category')

admin.site.register(Interest, InterestAdmin)

# --- NewsUser Model Admin ---
class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'bio')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('date_joined',)
    ordering = ('-date_joined',)

admin.site.register(Member, MemberAdmin)