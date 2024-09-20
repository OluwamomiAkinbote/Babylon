# admin.py
from django.contrib import admin
from .models import AdBanner

@admin.register(AdBanner)
class AdBannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'active', 'date')
    list_filter = ('category', 'active')
    search_fields = ('name',)
    readonly_fields = ('date',)
    list_editable = ('active',)
    # Include paragraph_positions in the fields displayed on the form
    fields = ('name', 'category', 'image_small', 'image_large', 'video', 'link', 'active', 'paragraph_positions', 'date')
    # Or, if you prefer using a custom form
    # form = AdBannerForm
