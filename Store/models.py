from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

# category model
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

# product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    image = models.ImageField(upload_to="uploads/product/")

    def __str__(self):
        return self.name
    

# customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="username")
    phone = models.CharField(max_length=20, unique=True, verbose_name="phone number")

    def __str__(self):
        return self.user.username


# customer orders model
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=200, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today, verbose_name="order date")
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name