from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name = 'cart'),
    path('add_to_cart/<slug:product_slug>/', views.add_to_cart, name = 'add_to_cart'),
    path('remove_cart_item/<slug:product_slug>/<int:cart_item_id>/', views.remove_cart_item, name = 'remove_cart_item'),
    path('decrement_cart_item/<slug:product_slug>/<int:cart_item_id>/', views.decrement_cart_item, name='decrement_cart_item'),
]
