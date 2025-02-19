from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name= 'products'), # if category__slug is None
    path('products/<slug:category_slug>/', views.products, name= 'products_by_category'), # if category__slug is not None
    path('product_detail/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name= 'product_detail'),
    path('search_items/', views.search, name= 'search_items'),
]
