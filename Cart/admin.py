from django.contrib import admin
from . models import Cart, cartItem

# Register your models here.

class cartAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart_id', 'date_added') # display the cart id and date added in the admin panel
    list_display_links = ('cart_id',)

class cartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'cart_name', 'quantity', 'is_active') # display the product, cart name, quantity, and is active in the admin panel
    list_display_links = ('product',)

admin.site.register(Cart, cartAdmin) # register the cart model with the cartAdmin class
admin.site.register(cartItem, cartItemAdmin) # register the cartItem model with the cartItemAdmin class
