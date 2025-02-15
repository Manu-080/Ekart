from django.db import models
from Store.models import Product, ProductVariation
from Accounts.models import Account

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id
    
class cartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartitem_product")
    variations = models.ManyToManyField(ProductVariation, blank=True, related_name="cartitem_variations")
    cart_name = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active  = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name