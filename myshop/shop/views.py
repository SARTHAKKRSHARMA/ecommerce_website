from django.shortcuts import render, get_object_or_404
from .models import Category, label, Product_SubCategory, Products
from cart.forms import CartAddProductForm
# # Create your views here.


def product_list(request,category_slug=None,subcategory_slug=None):
    category = None
    subcategory = None
    categories = Category.objects.all()
    products = []
    products_category = []
    product_1 = Products.objects.all()
    product_2 = Product_SubCategory.objects.all()
    
    

    
    if(category_slug):
        category = get_object_or_404(Category,slug=category_slug)
        product_1 = []
        product_2 = Product_SubCategory.objects.filter(category = category)
        product_3 = []
        for product in product_2:
            if(product.selling_price):
                product_3.append(product)  
        if(len(product_3) ==0):
            subcategory = []
            for product in product_2:
                subcategory.append(product)
            print(subcategory)
            product_1 = Products.objects.filter(category__in = subcategory)
    
    if(subcategory_slug):
        subcategory = get_object_or_404(Product_SubCategory,slug=subcategory_slug)
        product_1 = Products.objects.filter(category=subcategory)
        product_2 = []
        
        
    for product in product_1:
        products.append(product)
    
    for product in product_2:
        if(product.selling_price):
            products.append(product)
    
    return render(request,'shop/product/list.html',{'categories':categories,
                                                    'category':category,
                                                    'subcategory':subcategory,
                                                    'products':products})    


def product_detail(request, id, slug):
    try:
        product = get_object_or_404(Product_SubCategory, id=id, slug=slug)
        cart_product_form = CartAddProductForm()
        return render(request, 'shop/product/detail.html',{'product':product,'cart_product_form':cart_product_form})
    except:
        product = get_object_or_404(Products, id=id, slug=slug)
        cart_product_form = CartAddProductForm()
        return render(request, 'shop/product/detail.html',{'product':product,'cart_product_form':cart_product_form})
    
    
