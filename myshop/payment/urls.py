from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'payment'

urlpatterns = [
    path(_('process/'),views.option,name='process'),
    path(_('stripe/'),views.checkout,name='stripe'),
    path(_('cod/'),views.cod,name='cod'),
    path(_('success/'),views.payment_done,name='success'),
    path(_('charge/'),views.charge,name='charge'),
    path(_('cancel/'),views.payment_canceled,name='cancel')
]