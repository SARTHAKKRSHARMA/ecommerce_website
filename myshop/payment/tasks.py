from io import BytesIO
from celery import task
import pdfkit
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@task
def payment_completed(order_id):
    order = Order.objects.get(id = order_id)
    subject = f'My Shop -EE invoice no.{order.id}'
    message = 'Please, find attached invoice for your recent purchase'
    email = EmailMessage(subject,message,'admin@gmail.com',[order.email])
    context = Context({'order': order})
    context = context.flatten()
    html =render_to_string('order/order/pdf.html',context)
    out = BytesIO()
    pdfkit.from_string(html, 'out.pdf')
    pdf = open('out.pdf',mode='rb')
    response = HttpResponse(pdf.read(),content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=order_{order.id}.pdf'
    pdf.close()
    os.remove('out.pdf')
    email.attach(f'{response}','application/pdf')
    email.send()
