from django.shortcuts import render,redirect, get_object_or_404
from Store.models import Product, ProductVariation # import the Product model
from .models import Cart, cartItem

# Create your views here.

# function to get session key
def _cart_id(request):
    cart_id = request.session.session_key # get the existing session key
    if not cart:
        cart_id = request.session.create() # create a new session key if it does not exist
    return cart_id


def add_to_cart(request,product_slug): # add_to_cart view function
    # 1. Retrieve the Product
    product = get_object_or_404(Product, slug = product_slug) # get the product object by slug.

    # 2️. Extract Product Variations (Size, Color, etc.)
    product_variation = []

    if request.method == 'POST':
        for key, value in request.POST.items(): # for loop to get values from user using POST method.
            # (key = 'size' or 'variant' or 'color')
            # value = request.POST[key] | request.POST is a dictionary and returns value coresponding to key.
    
            try:
                variations = ProductVariation.objects.get(product = product, variation__iexact = key, variation_value__iexact = value)
                product_variation.append(variations)
            except ProductVariation.DoesNotExist:
                pass


    # 3️. get or create cart id.
    try: # if cart_id exists
        cartid = Cart.objects.get(cart_id = _cart_id(request)) # get the cart object by cart_id
    except Cart.DoesNotExist: # if cart_id does not exist create a new cart object
        cartid = Cart.objects.create(cart_id = _cart_id(request)) # create a new cart object
        cartid.save() 

    # 4. check if item exists in cart. 
    cart_items = cartItem.objects.filter(product = product, cart_name = cartid)

    # 5. If the Product Exists, Check Variations.
    if cart_items.exists() : 

        existing_variation_list = [list(item.variations.all()) for item in cart_items]
        item_ids = [item.id for item in cart_items]


        if product_variation in existing_variation_list:

            index = existing_variation_list.index(product_variation)
            item = cartItem.objects.get(product = product, id = item_ids[index])
            item.quantity += 1
            item.save()

        # 6. If the Product Exists but with a Different Variation.
        else:   
            
            item = cartItem.objects.create(product = product, quantity = 1, cart_name = cartid)
        

            if len(product_variation) > 0:
                item.variations.add(*product_variation)
            item.save()

    # 7. If the Product Does Not Exist in the Cart.
    else:
        cart_item = cartItem.objects.create(product = product, quantity = 1, cart_name = cartid) # create a new cartItem object 

        if len(product_variation) > 0:
            cart_item.variations.add(*product_variation)
        cart_item.save() # save the cartItem object
        
    return redirect('cart') # redirect to the cart page



""" This should be a javascript function in the cart.html template but i dont know how to do that yet"""
def remove_cart_item(request, product_slug, cart_item_id): # remove_cart_item view function
    cart = Cart.objects.get(cart_id = _cart_id(request)) 
    product = get_object_or_404(Product, slug = product_slug) # get the product object by id
    try:
        cart_item = cartItem.objects.get(product = product, cart_name = cart, id = cart_item_id) # get the cartItem object by product and cart_name
        
        cart_item.delete() # delete the cartItem object
    except:
        pass

    return redirect('cart') # redirect to the cart page


""" This should be a javascript function in the cart.html template but i dont know how to do that yet"""
def decrement_cart_item(request, product_slug, cart_item_id): # decrement_cart_item view function
    cartid = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, slug = product_slug)
    try:
        cart_item = cartItem.objects.get(product = product, cart_name = cartid, id = cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
    except:
        pass
    
    return redirect('cart') # redirect to the cart page



def cart(request, total = 0, cart_items = None): # cart view function
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request)) # get the cart object by cart_id = session key
        cart_items = cartItem.objects.filter(cart_name = cart, is_active = True) # get the cartItem objects by cart_name and is_active

        for cart_item in cart_items:
            if cart_item.product.stock <= 0: # if out of stock dont calculate total
                continue
            total += (cart_item.product.price * cart_item.quantity) # calculate the total price of all items in the cart using for loop.
        tax = (4 * total)/100 # calculate the tax
        total_amount = total + tax # calculate the total amount including tax

    except Cart.DoesNotExist:
       cart_items = []
       tax = 0
       total_amount = 0

    context = {
        'total': total,
        'cart_items': cart_items,
        'tax': tax,
        'total_amount': total_amount
    }
   
    return render(request, 'cart.html', context) # render the cart.html template