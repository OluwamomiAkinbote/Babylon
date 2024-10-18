from django.contrib import admin
from .models import Category, Product, ProductMedia, ProductVariant, FlashSale

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # Automatically populates slug from name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'sales_count', 'date', 'rating', 'is_in_stock')
    list_filter = ('category', 'date', 'rating', 'is_in_stock')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-date',)


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'video')
    search_fields = ('product__name',)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'variant_name', 'image', 'additional_price')
    search_fields = ('product__name', 'variant_name')


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
    search_fields = ('product__name',)



  





