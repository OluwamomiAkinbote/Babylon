from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from django.utils import timezone
import random
def shop_index(request):
    # Get category filter (if any)
    category_slug = request.GET.get('category', None)
    products = Product.objects.all()
    categories = Category.objects.filter(parent__isnull=True) 

    for product in products:
    
     product.star_range = range(5)  

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

        

    # Search functionality
    query = request.GET.get('search', '')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Sort by price, rating, etc.
    sort_by = request.GET.get('sort', 'date')  # Default to sort by date
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-date')

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'sort_by': sort_by,
    }
    return render(request, 'shop/shop_index.html', context)





def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.all()
    flash_sale = product.flash_sales.filter(start_time__lte=timezone.now(), end_time__gte=timezone.now()).first()
    media = product.media.all()

    # Fetch related products from the same category
    related_products_query = Product.objects.filter(category=product.category).exclude(id=product.id)
    related_products_list = list(related_products_query)  # Convert to list
    random.shuffle(related_products_list)  # Shuffle the list
    related_products = related_products_list[:6]  # Get the first 6 products

    context = {
        'product': product,
        'variants': variants,
        'flash_sale': flash_sale,
        'media': media,
        'related_products': related_products,  # Add related products to context
    }
    return render(request, 'shop/product_detail.html', context)



