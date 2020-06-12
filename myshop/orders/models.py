import stripe
from django.db import models
from shop.models import Products, Product_SubCategory
from decimal import Decimal
from django.core.validators import MaxValueValidator,MinValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Order(models.Model):
    first_name = models.CharField(_('first name'),max_length=50)
    last_name = models.CharField(_('last name'),max_length=50)
    email = models.EmailField(_('email'))
    address = models.CharField(_('address'),max_length=250)
    postal_code = models.CharField(_('postal code'),max_length=20)
    city = models.CharField(_('city'),max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=150, blank = True)
    coupon = models.ForeignKey(Coupon,related_name='orders',null=True,blank=True,on_delete=models.CASCADE)
    discount = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])
    
    class Meta:
        ordering = ('-created',)
        def __str__(self):
            return f'Order {self.id}'
        
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))   
    def charge(self, request, email, fee):
        # Set your secret key: remember to change this to your live secret key
        # in production. See your keys here https://manage.stripe.com/account
        stripe.api_key = 'sk_test_51GsWkmCqKsCKrXEpAvKcJUUob33FFYDeJhYc4W5iLMcusqqJZzMFoZfa2pIlB8fWDZVzi4k1AfSqDXUBVVGagYwe00VI5JJtLy'

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create a Customer
        stripe_customer = stripe.Customer.create(
            name=self.first_name,
            address=self.address,
            card=token,
            description=email
        )

       

        # Charge the Customer instead of the card
        stripe.Charge.create(
            amount=int(fee)*100, # in cents
            currency="rsd",
            description ='lovely descriptionsasa',
            customer=stripe_customer.id,
            
        )

        return stripe_customer

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products,on_delete=models.CASCADE,related_name='order_item',blank=True,null=True)
    products = models.ForeignKey(to=Product_SubCategory,on_delete=models.CASCADE,related_name='ordered_items',blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    weight = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price * self.weight



