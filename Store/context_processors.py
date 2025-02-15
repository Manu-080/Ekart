from .models import Category
from Cart.models import cartItem, Cart
from Cart.views import _cart_id
# In Django, context processors are functions that provide additional context data to templates. 
# They are used to make certain variables globally available in all templates without explicitly passing them in each view.

def category_links(request):
    return { 'links' : Category.objects.all() } # return the links as dictionary

def get_quantity(request, quantity = 0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = None  # Or create a new cart if needed
        
    cart_items = cartItem.objects.filter(cart_name = cart, is_active = True)

    for cart_item in cart_items:
        if cart_item.product.stock <= 0: # if out of stock dont calculate total quantity.
            continue
        quantity += cart_item.quantity # calculate the total quantity of all items in the cart using for loop.

    return {'total_quantity' : quantity} # return the quantity as dictionary