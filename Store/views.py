from django.shortcuts import render,get_object_or_404
from .models import Product,Category

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)[:8]
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)


# products page view
def products(request,category_slug=None): # category_slug is None by default
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug) # get the category object by slug
        products = Product.objects.filter(category = categories, is_available = True)
        product_count = products.count() # count the number of products from above query
    else:
        # if category_slug is None, then display all products
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count() # count the number of products from above query

    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request, 'products.html', context)

# product detail view
def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug = category_slug, slug = product_slug) # get the product object by category_slug and product_slug
    except Exception as e:
        raise e
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context) # render the product_detail.html template