from django.contrib import admin
from .models import Product_SubCategory, Category, Products, label
# Register your models here.

@admin.register(Product_SubCategory)
class Product_SubCategory_Admin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','slug','category','selling_price','available','dateOfEntry','expiryDate']
    list_filter = ['dateOfEntry','expiryDate']
    list_editable = ['selling_price','available']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','slug']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','slug','category','selling_price','available','dateOfEntry','expiryDate']
    list_filter = ['dateOfEntry','expiryDate','available']
    list_editable = ['selling_price','available']


@admin.register(label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['product_label','slug']
    prepopulated_fields = {'slug':('product_label',)}
