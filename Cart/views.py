from django.shortcuts import render,redirect, get_object_or_404
from Store.models import Product, ProductVariation # import the Product model
from .models import Carts, cartItem


# Create your views here.

# function to get session key
def _cart_id(request):
    cart_id = request.session.session_key # get the existing session key
    if not cart:
        cart_id = request.session.create() # create a new session key if it does not exist
        cart_id = request.session.session_key # get the new session key
    return cart_id


def add_to_cart(request,product_slug): # add_to_cart view function
    product = Product.objects.get(slug = product_slug) # get the product object by slug.
    product_variation = []

    if request.method == 'POST':
        for item in request.POST: # for loop to get values from user using POST method.
            key = item
            value = request.POST[key]
    
            try:
                variations = ProductVariation.objects.get(product = product, variation__iexact = key, variation_value__iexact = value)
                product_variation.append(variations)
            except:
                pass



    try: # if cart_id exists
        cartid = Carts.objects.get(cart_id = _cart_id(request)) # get the cart object by cart_id
    except Carts.DoesNotExist: # if cart_id does not exist create a new cart object
        cartid = Carts.objects.create(cart_id = _cart_id(request)) # create a new cart object
        cartid.save() 



    try: # if item exists in the cart.
        cart_item = cartItem.objects.get(product = product, cart_name = cartid) # get the cartItem object by product and cart_name

        if len(product_variation) > 0:
            for variation in product_variation:
                cart_item.variations.add(variation)


        cart_item.quantity += 1 # increment the quantity of the cartItem object by 1
        cart_item.save() # save the cartItem object
    except cartItem.DoesNotExist: # if item does not exist in the cart create a new cartItem object.
        cart_item = cartItem.objects.create(product = product, quantity = 1, cart_name = cartid) # create a new cartItem object 

        if len(product_variation) > 0:
            for variation in product_variation:
                cart_item.variations.add(variation)

        cart_item.save() # save the cartItem object
        
    return redirect('cart') # redirect to the cart page



""" This should be a javascript function in the cart.html template but i dont know how to do that yet"""
def remove_cart_item(request, product_slug): # remove_cart_item view function
    cart = Carts.objects.get(cart_id = _cart_id(request)) 
    product = get_object_or_404(Product, slug = product_slug) # get the product object by id
    cart_item = cartItem.objects.get(product = product, cart_name = cart) # get the cartItem object by product and cart_name
    
    cart_item.delete() # delete the cartItem object

    return redirect('cart') # redirect to the cart page


""" This should be a javascript function in the cart.html template but i dont know how to do that yet"""
def decrement_cart_item(request, product_slug): # decrement_cart_item view function
    cartid = Carts.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, slug = product_slug)
    cart_item = cartItem.objects.get(product = product, cart_name = cartid)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    
    return redirect('cart') # redirect to the cart page



def cart(request, total = 0, cart_items = None): # cart view function
    try:
        cart = Carts.objects.get(cart_id = _cart_id(request)) # get the cart object by cart_id = session key
        cart_items = cartItem.objects.filter(cart_name = cart, is_active = True) # get the cartItem objects by cart_name and is_active

        for cart_item in cart_items:
            if cart_item.product.stock <= 0: # if out of stock dont calculate total
                continue
            total += (cart_item.product.price * cart_item.quantity) # calculate the total price of all items in the cart using for loop.
        tax = (4 * total)/100 # calculate the tax
        total_amount = total + tax # calculate the total amount including tax

    except Carts.DoesNotExist:
        pass # pass the exception if the cart object does not exist

    context = {
        'total': total,
        'cart_items': cart_items,
        'tax': tax,
        'total_amount': total_amount
    }
   
    return render(request, 'cart.html', context) # render the cart.html template