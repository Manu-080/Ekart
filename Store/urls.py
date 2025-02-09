from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name = 'products'),
    path('<slug:category_slug>/', views.products, name = 'products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name = 'product_detail'),
]
