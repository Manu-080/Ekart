from django.contrib import admin
from .models import Category, Product, ProductVariation

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug') # display the category name and slug in the admin panel
    prepopulated_fields = {'slug' : ('category_name',)} # automatically populate the slug field with the category name
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'modified_date', 'is_available')# display the product name, price, stock, category, created date, modified date, and availability in the admin panel
    prepopulated_fields = {'slug' : ('product_name',)} # automatically populate the slug field with the product name
    ordering = ['-created_date'] # order the products by craeted date in descending order

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation', 'is_active', 'created_date',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation', 'is_active', 'created_date',)
    
admin.site.register(Category, CategoryAdmin) # register the Category model with the CategoryAdmin class
admin.site.register(Product, ProductAdmin) # register the Product model with the ProductAdmin class
admin.site.register(ProductVariation, ProductVariationAdmin)
