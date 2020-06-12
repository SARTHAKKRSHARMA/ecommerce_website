from django import forms
from django.utils.translation import gettext_lazy as _
PRODUCT_WEIGHT_CHOICES = [(i,str(i)) for i in range(1,50)]

class CartAddProductForm(forms.Form):
    weight = forms.TypedChoiceField(choices=PRODUCT_WEIGHT_CHOICES,coerce=int,label=_('Weight'))
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
