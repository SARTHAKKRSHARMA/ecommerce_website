import os
import pdfkit
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, Order
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.template import Context
# Create your views here.
@staff_member_required
def admin_order_detail(request, order_id):
    order =get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html',{'order':order})

@staff_member_required
def admin_order_pdf(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    context = Context({'order': order})
    context = context.flatten()
    html =render_to_string('order/order/pdf.html',context)
    pdfkit.from_string(html, 'out.pdf')
    pdf = open('out.pdf',mode='rb')
    response = HttpResponse(pdf.read(),content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=order_{order.id}.pdf'
    pdf.close()
    os.remove('out.pdf')
    return response




def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if(form.is_valid):
            order = form.save(commit=False)
            if(cart.coupon):
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                try:
                    OrderItem.objects.create(order=order,product=item['product'],price=item['price'],weight=item['weight'])
                except:
                    OrderItem.objects.create(order=order,products=item['product'],price=item['price'],weight=item['weight'])
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
        return render(request,'order/order/create.html',{'cart':cart,'form':form})
