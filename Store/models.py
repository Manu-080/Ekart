from django.db import models
from django.urls import reverse

# Create your models here.

# category model
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_url(self):
        return reverse('products_by_category', args=[self.slug]) # products_by_category is the name of the URL pattern in urls.py

    def __str__(self):
        return self.category_name
    

# product model
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="product_category")
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    image = models.ImageField(upload_to="uploads/product/")
    priority = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug]) # product_detail is the name of the URL pattern in urls.py
    

    def __str__(self):
        return self.product_name
    

class ProductVariationManager(models.Manager):
    def colors(self):
        return self.filter(variation = 'color', is_active= True)
    
    def sizes(self):
        return self.filter(variation = 'size', is_active= True)
    
    def variants(self):
        return self.filter(variation = 'variant', is_active = True)


variation_choices = (
        ('color','Color'),
        ('size','Size'),
        ('variant', 'Variant')
)

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variation')
    variation = models.CharField(max_length=100, choices=variation_choices, null=True)
    variation_value =models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)


    objects = ProductVariationManager()
    
    def __str__(self):
        return self.variation_value