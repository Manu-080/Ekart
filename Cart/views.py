from django.shortcuts import render,redirect
from Store.models import Product # import the Product model
from .models import Carts, cartItem

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request,product_id): # add_to_cart view function
    product = Product.objects.get(id = product_id) # get the product object by id
    try:
        cart_obj = Carts.objects.get(cart_id = _cart_id(request)) # get the cart object by cart_id
    except Carts.DoesNotExist:
        cart_obj = Carts.objects.create(cart_id = _cart_id(request)) # create a new cart object
        cart_obj.save() 

    try:
        cart_item = cartItem.objects.get(product = product, cart_name = cart_obj) # get the cartItem object by product and cart_name
        cart_item.quantity += 1 # increment the quantity of the cartItem object by 1
        cart_item.save() # save the cartItem object
    except cartItem.DoesNotExist:
        cart_item = cartItem.objects.create(product = product, quantity = 1, cart_name = cart_obj) # create a new cartItem object 
        cart_item.save() # save the cartItem object
        
    return redirect('cart') # redirect to the cart page


def cart(request, total = 0, quantity = 0, cart_items = None): # cart view function
    try:
        cart = Carts.objects.get(cart_id = _cart_id(request)) # get the cart object by cart_id
        cart_items = cartItem.objects.filter(cart_name = cart, is_active = True) # get the cartItem objects by cart_name and is_active
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except Carts.DoesNotExist:
        pass # pass the exception if the cart object does not exist

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
   
    return render(request, 'cart.html', context) # render the cart.html template