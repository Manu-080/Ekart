from django.shortcuts import render,get_object_or_404
from .models import Product,Category,ProductVariation
from Cart.models import cartItem, Carts
from django.core.paginator import Paginator

from Cart.views import _cart_id

# Create your views here.

def home(request):
    products = Product.objects.filter(is_available=True).order_by('priority')[:8]
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)



# products page view
def products(request,category_slug=None): # category_slug is None by default
    
    # to get products by category
    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug) # get the category object by slug
        products = Product.objects.filter(category = categories, is_available = True)
        product_count = products.count() # count the number of products from above query
    else:
        # if category_slug is None, then display all products
        products = Product.objects.filter(is_available=True)
        product_count = products.count() # count the number of products from above query

    paginator = Paginator(products, 9) # show 8 products per page
    page_number = request.GET.get('page') # get the page number from the url
    page_obj = paginator.get_page(page_number) # get the products for the page number

    context = {
        #'products' : products,
        'product_count' : product_count,
        'products': page_obj,
    }
    return render(request, 'products.html', context)



# product detail view
def product_detail(request, category_slug, product_slug):
    product_variation = []
    if request.POST:
        for items in request.POST:
            key = items
            value = request.POST[key]

            try:
                variations = ProductVariation.objects.get(product = product, variation__iexact = key, variation_value__iexact = value)
                product_variation.append(variations)
            except:
                pass


    try:
        product = Product.objects.get(category__slug = category_slug, slug = product_slug) # get the product object by category.slug and product.slug
        # to check if the product is already in the users cart.
        in_cart = cartItem.objects.filter(cart_name = Carts.objects.get(cart_id = _cart_id(request)), product = product).exists() # can also write cart_name__cart_id = _cart_id(request)
        
    except Exception as e:
        raise e
    context = {
        'product': product,
        'in_cart': in_cart,
    }
    return render(request, 'product_detail.html', context) # render the product_detail.html template


def search(request):
    if request.method == 'GET':
        search_item = request.GET.get('keyword')
        if not search_item or len(search_item) > 30:
            search_output = Product.objects.none() # search output is none.
        else:
            search_output = Product.objects.filter(product_name__icontains = search_item) # search output contains some values.

    if search_output:
        product_count = search_output.count() # count the number of products from above query
    else:
        product_count = 0

    context = {
        'products':search_output,
        'product_count':product_count,
    }

    return render(request, 'products.html', context)