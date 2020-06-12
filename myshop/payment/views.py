import stripe
from django.shortcuts import render, get_object_or_404
from orders.models import Order
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from .tasks import payment_completed    
stripe.api_key = 'sk_test_51GsWkmCqKsCKrXEpAvKcJUUob33FFYDeJhYc4W5iLMcusqqJZzMFoZfa2pIlB8fWDZVzi4k1AfSqDXUBVVGagYwe00VI5JJtLy'    

def option(request):    
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    if(request.POST):
        value = request.POST['payment']
        if(value =='byStripe'):
            return HttpResponseRedirect(reverse('payment:stripe'))
        elif(value=='cod'):
            return HttpResponseRedirect(reverse('payment:cod'))
        # else:
        #     return HttpResponseRedirect(reverse('payment:paypay'))
        return render(request,'option.html',{'total_cost':total_cost})
    return render(request,'option.html',{'total_cost':total_cost})

def cod(request):
    pass


def checkout(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    return render(request,'checkout.html',{'total_cost':total_cost})

def charge(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = int(order.get_total_cost()) * 100
    if(request.POST):
        source = request.POST['stripeToken']
        name = request.POST['name']
        email = request.POST['email']
        city = request.POST['city']
        country = request.POST['country']
        line1 = request.POST['line1']
        line2 = request.POST['line2']
        postal_code = request.POST['postal_code']
        state = request.POST['state']
        

            # customer = stripe.Customer.create(
            #         description = 'MtnameisKhanImnotaterrorist'
            # )
        try:
            customer = stripe.Customer.create(
                description = 'MyNameisKhan',
                source = source,
                name = name,
                email = email
            )

            stripe.Charge.create(
                customer = customer,
                amount = total_cost,
                currency = 'usd',
                description = 'Payment for order',
                shipping = {
                    "address": {
                        "city": city,
                        "country": country,
                        "line1": line1,
                        "line2": line2,
                        "postal_code": postal_code,
                        "state": state
                    },
                    "name": name,
                },    
            )
        
            order.paid = True
            order.save()
            payment_completed.delay(order.id) 
            return HttpResponseRedirect(reverse('payment:success'))
        except :
            return HttpResponseRedirect(reverse('payment:cancel'))
            

def payment_done(request):
    return render(request, 'done.html')

def payment_canceled(request):
    return render(request,'cancelled.html')

