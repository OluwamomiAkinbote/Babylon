from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_index, name='shop_index'),
    path('product-details<slug:slug>/', views.product_detail, name='product_detail'),
  
]