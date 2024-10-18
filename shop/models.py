from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)  # Required slug
    parent = models.ForeignKey(
        'self', 
        related_name='subcategories', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name_plural = "Categories"  # Plural form for admin display
        unique_together = ('name', 'parent')  # Ensures no duplicate names under the same parent

    def __str__(self):
        return self.name

    def get_subcategories(self):
        """Returns all subcategories of this category."""
        return self.subcategories.all()

    @property
    def is_subcategory(self):
        """Checks if the category has a parent, indicating it's a subcategory."""
        return self.parent is not None

    def save(self, *args, **kwargs):
        """Automatically generates a slug from the category name if not provided."""
        if not self.slug:  # Only generate slug if it's not already set
            self.slug = slugify(self.name)  
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = HTMLField()
    price = models.IntegerField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name='products')  # Main product image
    rating = models.DecimalField(max_digits=2, decimal_places=1, choices=[(i / 2, f"{i / 2}") for i in range(0, 11)], default=0.0)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    sales_count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_in_stock = models.BooleanField(default=True)
    url = models.URLField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.is_in_stock = self.stock_quantity > 0
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def average_rating(self):
        # Implement logic if you're tracking multiple ratings
        return self.rating

    def __str__(self):
        return self.name
    
    @property
    def formatted_price(self):
        return f"₦{self.price:,.2f}"

    @property
    def formatted_discount_price(self):
        if self.discount_price:
            return f"₦{self.discount_price:,.2f}"  
        return None

    @property
    def formatted_sales_count(self):
        return f"{self.sales_count:,}" 



class ProductMedia(models.Model):
    product = models.ForeignKey(Product, related_name='media', on_delete=models.CASCADE)
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name='product_images')
    video = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL, related_name='product_videos')

    def __str__(self):
        return f"Media for {self.product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=100) 
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name='product_variant')
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def __str__(self):
        return f"{self.variant_name} for {self.product.name}"
    
class FlashSale(models.Model):
    product = models.ForeignKey(Product, related_name='flash_sales', on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField(blank=True, null=True)  # Make it optional to manually input
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Calculate the discount percentage if discount_price exists and is lower than the price
        if self.product.discount_price and self.product.discount_price < self.product.price:
            self.discount_percentage = int(((self.product.price - self.product.discount_price) / self.product.price) * 100)
        else:
            self.discount_percentage = 0  # No discount if no valid discount_price

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Flash sale for {self.product.name} ({self.discount_percentage}% off)"
