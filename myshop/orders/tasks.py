from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    order = Order.objects.get(id=order_od)
    subject = f'Order no. {order.id}'
    message = f'Dear {order.first_name},\n\n'\
        f"You've successfully placed an order"\
        f"You order ID is {order.id}."
    
    mail_sent = send_mail(subject, message,'admin@myshop.com',[order.email])
    return mail_sent