from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Products, Product_SubCategory
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
# Create your views here.

@require_POST
def cart_add(request, product_id, product_slug):
    cart = Cart(request)
    try:
        product = get_object_or_404(Products,id=product_id,slug=product_slug)
    except:
        product = get_object_or_404(Product_SubCategory,id=product_id,slug=product_slug)

    form = CartAddProductForm(request.POST)
    if(form.is_valid()):
        cd = form.cleaned_data
        cart.add(product=product,weight=cd['weight'],override_quantity=cd['override'])

    return redirect('cart:cart_detail')    

@require_POST
def cart_remove(request, product_id,product_slug):
    cart = Cart(request)
    try:
        product = get_object_or_404(Products,id=product_id, slug=str(product_slug))
    except:
        product = get_object_or_404(Product_SubCategory,id=product_id, slug=product_slug)
    
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'weight':item['weight'],
            'override':True
        })
    coupon_apply_form = CouponApplyForm()
    return render(request,'cart/detail.html',{'cart':cart,'coupon_apply_form':coupon_apply_form})
