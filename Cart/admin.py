from django.contrib import admin
from . models import Carts, cartItem

# Register your models here.

class cartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added') # display the cart id and date added in the admin panel

class cartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart_name', 'quantity', 'is_active') # display the product, cart name, quantity, and is active in the admin panel

admin.site.register(Carts, cartAdmin) # register the cart model with the cartAdmin class
admin.site.register(cartItem, cartItemAdmin) # register the cartItem model with the cartItemAdmin class
