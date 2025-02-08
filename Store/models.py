from django.db import models

# Create your models here.

# category model
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name
    

# product model
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    image = models.ImageField(upload_to="uploads/product/")
    priority = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
